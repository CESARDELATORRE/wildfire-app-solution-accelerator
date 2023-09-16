from dapr.ext.grpc import App, InvokeMethodRequest, InvokeMethodResponse

from src.inference import main
import json
import logging
import sys

app = App()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

@app.method(name='frames-receiver')
def framesreceiver(request: InvokeMethodRequest) -> InvokeMethodResponse:
    
    logging.info(f'Frame received')
    
    frame = json.loads(request.text())['image']
    source_id = json.loads(request.text())['source_id']
    timestamp = json.loads(request.text())['timestamp']
    time_trace = json.loads(request.text())['time_trace']

    detection_threshold=0.0

    path='events_schema/detections.avro'

    main(source_id, timestamp, frame, detection_threshold, path, time_trace)

    return InvokeMethodResponse(b'Frame Analyzed', "text/plain; charset=UTF-8")

app.run(2060)