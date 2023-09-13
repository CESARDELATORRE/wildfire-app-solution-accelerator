from dapr.clients import DaprClient
import time
import json
import base64
import cv2
import numpy as np
import avro.schema
from avro_json_serializer import AvroJsonSerializer
import logging

import os
import pandas as pd
# import base64
import mlflow.pyfunc


def PublishEvent (pubsub_name: str, topic_name: str, data: json):
    with DaprClient() as client:
        resp = client.publish_event(pubsub_name=pubsub_name, topic_name=topic_name, data=data, data_content_type='application/json')

def read_image(image_path):
    with open(image_path, "rb") as f:
        return f.read()       

# OLD function definition with OLD model
# def main(source_id, timestamp, model, frame, detection_threshold, path, time_trace):

# New function with no model parameter, but faking it.
def main(source_id, timestamp, frame, detection_threshold, path, time_trace):
    timestamp_init=int(time.time()*1000)
    logging.basicConfig(level=logging.DEBUG)
    logging.info(source_id)

    ################################################
    # OLD code to read the image from the frame coming from the network

    # Decode the base64 encoded image
    backToBytes = base64.standard_b64decode(frame)
    img = cv2.imdecode(np.frombuffer(backToBytes, np.uint8), cv2.IMREAD_COLOR)

    val_to_compare_resize,_,_=img.shape
    
    if val_to_compare_resize>576:
        logging.info(f'Resizing to print')
        dim = (720,576)
        img= cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        frame_resized = cv2.imencode(".jpg", img)[1]
        frame_to_bytes=frame_resized.tobytes()
        frame = base64.standard_b64encode(frame_to_bytes)
        frame = frame.decode()

    data = { "SourceId":source_id,
    "UrlVideoEncoded": "1.0",
    "Frame": frame,
    "EventName": "ObjectDetection",
    "OriginModule": "Ai inference detection",
    "Information": "Test message",
    "EveryTime": int(timestamp),
    "Classes": [],
    "time_trace":[]
    }
    data['time_trace'].append(time_trace)

    #######################################################################
    # NEW Model inference

    # Local dir where you have downloaded and saved the artifacts
    local_dir = "."
    mlflow_model_dir = os.path.join(local_dir, "mlflow-model")

    logging.info(f'MLFlow model directory: {mlflow_model_dir}')

    # Show the contents of the MLFlow model folder
    dir_content = os.listdir(mlflow_model_dir)
    logging.info(f'MLFlow model directory content: {dir_content}')

    ## Load Test Image FILES for testing the model
    #dataset_parent_dir = "./test_images"
    #dataset_name = "odFridgeObjects"
    #
    #test_image_paths = [
    #    os.path.join(dataset_parent_dir, dataset_name, "images", "1.jpg")
    #]
    #
    #logging.info(f'Test images: {test_image_paths}')
    #
    #test_df = pd.DataFrame(
    #    data=[
    #        base64.encodebytes(read_image(image_path)).decode("utf-8")
    #        for image_path in test_image_paths
    #    ],
    #    columns=["image"],
    #)

    # Convert the image into a DataFrame with a single row
    test_df = pd.DataFrame(data=[base64.encodebytes(cv2.imencode('.jpg', img)[1]).decode("utf-8")], columns=["image"])

    logging.info(f'Test DataFrame shape: {test_df.shape}')

    # Instantiate the MLFlow model from the downloaded MLFlow model files
    pyfunc_model = mlflow.pyfunc.load_model(mlflow_model_dir)

    # Use the DataFrame for model prediction
    prediction_result = pyfunc_model.predict(test_df)

    logging.info(f'prediction_result: |START|{prediction_result}|END|')


    #######################################################################

    # OLD Model inference
    # results = model(img)
    # logging.info(f'Model inference results: |START|{results}|END|')
    # Take only first element
    # detections = json.loads(results.pandas().xyxy[0].to_json())

    # Mocking model with hardcoded detections for testing and getting rid of old model
    json_string = '{"xmin": {"0": 273.964263916}, "ymin": {"0": 36.4909439087}, "xmax": {"0": 311.4987182617}, "ymax": {"0": 165.910369873}, "confidence": {"0": 0.7896723747}, "class": {"0": 0}, "name": {"0": "person"}}'
    detections = json.loads(json_string)

    logging.info(f'Model inference JSON: |START|{detections}|END|')
    
    # Tracing the Obj Detection JSON
    if "name" in detections and detections["name"]:
        # Access the value of the "name" key
        name = detections["name"]["0"]
        print(f"The object detection class name is {name}")
    else:
        print("The name key does not exist or is empty")
    
    if detections["name"]!={}:
        logging.info(f'Objects Detected')
        
        for idx,detection in enumerate(detections["name"].values()):
            
            BoundingBoxes=[]
            
            if list(detections["confidence"].values())[idx] > detection_threshold:
                
                xmin=list(detections["xmin"].values())[idx]
                xmax=list(detections["xmax"].values())[idx]
                ymin=list(detections["ymin"].values())[idx]
                ymax=list(detections["ymax"].values())[idx]
                BoundingBoxes.append({"x": xmin, "y":ymin})
                BoundingBoxes.append({"x": xmin, "y":ymax})
                BoundingBoxes.append({"x": xmax, "y":ymin})
                BoundingBoxes.append({"x": xmax, "y":ymax})
     
                data["Classes"].append({"EventType": detection, "Confidence":list(detections["confidence"].values())[idx], "BoundingBoxes": BoundingBoxes})
    
        data['time_trace'].append({"stepStart": timestamp_init, "stepEnd":int(time.time()*1000), "stepName": "ai_inferencer"})
        
        schema = avro.schema.Parse(open(path, "rb").read())
        serializer = AvroJsonSerializer(schema)
    
        json_str = serializer.to_json(data)
     
        PublishEvent(pubsub_name="pubsub", topic_name="newDetection", data=json_str)
        logging.info(f'Event published')

    return 




