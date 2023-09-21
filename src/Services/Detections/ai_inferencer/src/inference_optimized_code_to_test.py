import os
import base64
import cv2
import pandas as pd
import logging
import json
import time
import avro.schema
from avro_json_serializer import AvroJsonSerializer
import mlflow.pyfunc

from dapr.clients import DaprClient

def PublishEvent(pubsub_name: str, topic_name: str, data: json):
    with DaprClient() as client:
        resp = client.publish_event(pubsub_name=pubsub_name, topic_name=topic_name, data=data, data_content_type='application/json')

def main(source_id, timestamp, frame, detection_threshold, path, time_trace):
    timestamp_init=int(time.time()*1000)
    logging.basicConfig(level=logging.DEBUG)
    logging.info(source_id)

    # Decode the base64 encoded image
    backToBytes = base64.standard_b64decode(frame)
    img = cv2.imdecode(np.frombuffer(backToBytes, np.uint8), cv2.IMREAD_COLOR)

    # Dimension of the image needed to calculate the bounding boxes coordinates in the right units
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

    #############################################################################
    # Model inference with AutoML computer vision model expoerted as MLFlow model

    # Local dir where you have downloaded and saved the artifacts
    local_dir = "."
    mlflow_model_dir = os.path.join(local_dir, "mlflow-model")

    logging.info(f'MLFlow model directory: {mlflow_model_dir}')

    # Show the contents of the MLFlow model folder
    dir_content = os.listdir(mlflow_model_dir)
    logging.info(f'MLFlow model directory content: {dir_content}')

    # Convert the image into a DataFrame with a single row
    test_df = pd.DataFrame(data=[base64.b64encode(cv2.imencode('.jpg', img)[1]).decode("utf-8")], columns=["image"])

    logging.info(f'Test DataFrame shape: {test_df.shape}')

    # Instantiate the MLFlow model from the downloaded MLFlow model files
    pyfunc_model = mlflow.pyfunc.load_model(mlflow_model_dir)

    # Use the DataFrame for model prediction
    prediction_result = pyfunc_model.predict(test_df)

    logging.info(f'TYPE of prediction_result: {type(prediction_result)}')

    # Convert the prediction result to the required data structure
    data = {"Classes": [], "time_trace": []}
    timestamp_init = int(time.time()*1000)

    if prediction_result:
        logging.info(f'Objects Detected')
        
        for detection in prediction_result[0]["boxes"]:
            
            BoundingBoxes=[]
            
            if detection["score"] > detection_threshold:
                
                # In this object detection models, the output bounding box coordinates are normalized, 
                # meaning they are given as a proportion of the image's width and height, 
                # rather than in pixels. The values are typically in the range [0, 1], where (0, 0) 
                # represents the top-left corner of the image, and (1, 1) represents the bottom-right corner.
                # Hence, the calculations below are needed to get the real bounding box coordinates in pixels.

                xmin = detection["box"]["topX"] * width
                xmax = detection["box"]["bottomX"] * width
                ymin = detection["box"]["topY"] * height
                ymax = detection["box"]["bottomY"] * height

                BoundingBoxes.append({"x": xmin, "y":ymin})
                BoundingBoxes.append({"x": xmin, "y":ymax})
                BoundingBoxes.append({"x": xmax, "y":ymin})
                BoundingBoxes.append({"x": xmax, "y":ymax})

                data["Classes"].append({"EventType": detection["label"], "Confidence":detection["score"], "BoundingBoxes": BoundingBoxes})

        data['time_trace'].append({"stepStart": timestamp_init, "stepEnd":int(time.time()*1000), "stepName": "ai_inferencer"})
    
        schema = avro.schema.Parse(open(path, "rb").read())
        serializer = AvroJsonSerializer(schema)
    
        json_str = serializer.to_json(data)

        # Logging the Event JSON string
        # logging.info(f'Event AVRO JSON string: |START|{json_str}|END|')
     
        PublishEvent(pubsub_name="pubsub", topic_name="newDetection", data=json_str)
        logging.info(f'Event published')

    return 
