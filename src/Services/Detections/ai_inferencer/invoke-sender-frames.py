from dapr.ext.grpc import App, InvokeMethodRequest, InvokeMethodResponse

# Removed since we won't directly use Pytorch
# import torch

from src.inference import main
import json
import logging
import sys

app = App()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# Removed the OLD MODEL
#global model 
# model = torch.hub.load("ultralytics/yolov5", "yolov5s")

@app.method(name='frames-receiver')
def framesreceiver(request: InvokeMethodRequest) -> InvokeMethodResponse:
    
    logging.info(f'Frame received')
    
    # (CDLTLL) Original code without AutoML model
    #
    frame = json.loads(request.text())['image']
    source_id = json.loads(request.text())['source_id']
    timestamp = json.loads(request.text())['timestamp']
    time_trace = json.loads(request.text())['time_trace']

    detection_threshold=0.0

    path='events_schema/detections.avro'

    # NEW call with mocked model inference / later AutoML model
    main(source_id, timestamp, frame, detection_threshold, path, time_trace)

    # OLD call with OLD model
    # main(source_id, timestamp, model, frame, detection_threshold, path, time_trace)

    return InvokeMethodResponse(b'Frame Analyzed', "text/plain; charset=UTF-8")

app.run(2060)