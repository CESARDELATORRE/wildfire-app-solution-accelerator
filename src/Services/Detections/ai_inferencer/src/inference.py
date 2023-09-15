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

# New function with no model parameter, but faking it.
def main(source_id, timestamp, frame, detection_threshold, path, time_trace):
    timestamp_init=int(time.time()*1000)
    logging.basicConfig(level=logging.DEBUG)
    logging.info(source_id)

    # Decode the base64 encoded image
    backToBytes = base64.standard_b64decode(frame)
    img = cv2.imdecode(np.frombuffer(backToBytes, np.uint8), cv2.IMREAD_COLOR)

    # (CDLTLL) This tunning needs to be confirmed before using it
    # Resize the image to a fixed size to the model's input size so performance increases
    # val_to_compare_resize,_,_=img.shape
    # if val_to_compare_resize>576:
    #     logging.info(f'Resizing to fit model's input size so performance increases')
    #     dim = (720,576)
    #     img= cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    #     frame_resized = cv2.imencode(".jpg", img)[1]
    #     frame_to_bytes=frame_resized.tobytes()
    #     frame = base64.standard_b64encode(frame_to_bytes)
    #     frame = frame.decode()

    # (CDLTLL)
    # Dimension of the image needed to calculate the bounding boxes coordinates in the right units
    # Need to get it after the possible image resize, otherwise the coordinates will be wrong positioned
    height, width = img.shape[:2]

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

    ## JUST FOR TESTING BUT NOT NEEDED, WE ARE NOT USING A DATASET WITH IMAGE FILES 
    # BUT AN IMAGE COMING FROM THE STREAMING/NETWORK
    ## Load Test Image files for testing the model
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

    logging.info(f'TYPE of prediction_result: {type(prediction_result)}')
    
    # Set the display options
    pd.set_option('display.max_columns', None)  # None means unlimited
    pd.set_option('display.expand_frame_repr', False)  # Don't wrap to multiple lines
    pd.set_option('max_colwidth', -1)  # Full column width

    # Now show the full DataFrame
    logging.info(f'prediction_result CONTENT: |START|{prediction_result}|END|')

    # Reset the display options to default
    pd.reset_option('display.max_columns')
    pd.reset_option('display.expand_frame_repr')
    pd.reset_option('max_colwidth')

    # example_prediction_result_json = '[{"boxes":[{"box":{"topX":0.1843043566,"topY":0.1406233013,"bottomX":0.4368721962,"bottomY":0.6701216698},"label":"carton","score":0.8811187744},{"box":{"topX":0.3369935513,"topY":0.567420125,"bottomX":0.878276062,"bottomY":0.7225573063},"label":"milk_bottle","score":0.7880781889}]}]'

    # Initialize an empty dictionary to store all detections
    detections = {
        'xmin': {},
        'ymin': {},
        'xmax': {},
        'ymax': {},
        'confidence': {},
        'class': {},
        'name': {}
    }

    # Loop over each list in the 'boxes' column
    for i, boxes in enumerate(prediction_result['boxes']):
        # Loop over each detection in the list
        for j, detection in enumerate(boxes):
            # Add the detection to the detections dictionary
            detections['xmin'][str(j)] = detection['box']['topX']
            detections['ymin'][str(j)] = detection['box']['topY']
            detections['xmax'][str(j)] = detection['box']['bottomX']
            detections['ymax'][str(j)] = detection['box']['bottomY']
            detections['confidence'][str(j)] = detection['score']
            detections['class'][str(j)] = 0  # Assuming class is always 0
            
            detections['name'][str(j)] = detection['label']  # Real label name
            # detections['name'][str(j)] = 'person'  # Faked label name

    # Now detections is a dictionary representing all detections
    logging.info(f'Detections Dictionary: |START|{detections}|END|')

    if detections["name"]!={}:
        logging.info(f'Objects Detected')
        
        for idx, detection in enumerate(detections["name"].values()):
            
            BoundingBoxes=[]
            
            if list(detections["confidence"].values())[idx] > detection_threshold:
                
                # REAL BOUNDING BOXES
                # In this object detection models, the output bounding box coordinates are normalized, 
                # meaning they are given as a proportion of the image's width and height, 
                # rather than in pixels. The values are typically in the range [0, 1], where (0, 0) 
                # represents the top-left corner of the image, and (1, 1) represents the bottom-right corner.
                # Hence, the calculations below are needed to get the real bounding box coordinates in pixels.

                normalized_xmin = list(detections["xmin"].values())[idx]
                normalized_xmax = list(detections["xmax"].values())[idx]
                normalized_ymin = list(detections["ymin"].values())[idx]
                normalized_ymax = list(detections["ymax"].values())[idx]

                xmin =  normalized_xmin * width
                xmax =  normalized_xmax * width
                ymin =  normalized_ymin * height
                ymax =  normalized_ymax * height

                # Logging the REAL Bounding Boxes
                logging.info(f'REAL BOUNDING BOXES: |START|xmin:{xmin},xmax:{xmax},ymin:{ymin},ymax:{ymax}|END|')
                
                # FIXED/FAKED BOUNDING BOXES
                # xmin=273.964263916
                # xmax=311.4987182617
                # ymin=36.4909439087
                # ymax=165.910369873
                # Logging the FAKED Bounding Boxes
                # logging.info(f'FAKED BOUNDING BOXES: |START|xmin:{xmin},xmax:{xmax},ymin:{ymin},ymax:{ymax}|END|')

                BoundingBoxes.append({"x": xmin, "y":ymin})
                BoundingBoxes.append({"x": xmin, "y":ymax})
                BoundingBoxes.append({"x": xmax, "y":ymin})
                BoundingBoxes.append({"x": xmax, "y":ymax})

                data["Classes"].append({"EventType": detection, "Confidence":list(detections["confidence"].values())[idx], "BoundingBoxes": BoundingBoxes})

        data['time_trace'].append({"stepStart": timestamp_init, "stepEnd":int(time.time()*1000), "stepName": "ai_inferencer"})
    
        schema = avro.schema.Parse(open(path, "rb").read())
        serializer = AvroJsonSerializer(schema)
    
        json_str = serializer.to_json(data)

        # Logging the Event JSON string
        # logging.info(f'Event AVRO JSON string: |START|{json_str}|END|')
     
        PublishEvent(pubsub_name="pubsub", topic_name="newDetection", data=json_str)
        logging.info(f'Event published')

    return 




