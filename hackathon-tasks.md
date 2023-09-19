


# Sub-Teams

- **AI/ML team:** AI model training and dataset labeling.
- **Dev team:** Model inference integration in Docker container. Alert rules implementation, etc.
- **Story telling and media team:** Story narrative, interviews to the team and video editing.

# Main tasks

| | |
|--------|--------|
| **1. AI/ML motion** | - 1.1 Find or create a Labeled fire/smoke images Dataset (For Object Detection) - 1.2 Create/Train AI Model for detecting fire & smoke |
| **2. Dev motion** | - 2.1 Integrate AI Model within the AI.Inference Python microservice - 2.2 Create custom “Alert Rules” specific for the “wildfire domain” |
| **3. Story motion**| - 3.1 Create the "Story narrative" - 3.2 Record interviews to the members of the project - 3.3 Edit video and create the final "Project story video" to be provided as our deliverable of the Hackathon.|

## Guidelines for AI/ML tasks

### Create AI Model for detecting fire & smoke 

#### Train a new Object Detection model for detecting fire and smoke classes. Possible approaches:

**OPTION A (PREFERRED): AutoML for computer vision models**

Azure Machine Learning AutoML for computer vision models automatically does transfer learning from these foundation object detection models: YOLOv5, ResNet, RetinaNet (multiple trainings trying these foundation models with different hyperparameter combinations)

*AutoML computer vision Tutorials (Learning "How to"):*
      
https://learn.microsoft.com/en-us/azure/machine-learning/how-to-auto-train-image-models?view=azureml-api-2&tabs=cli   
      
https://learn.microsoft.com/en-us/azure/machine-learning/how-to-use-automl-small-object-detect?view=azureml-api-2&tabs=CLI-v2 

*AutoML computer vision Jupyter notebooks (Using AML SDK):*

*For training the model (Data Scientists / ML Engineer):*
[Training an Object Detection model with AutoML](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/automl-image-object-detection-task-fridge-items.ipynb)

*For inference with the model and make predictions (Developers / ML Engineer):*
[Inference model locally with MLFlow](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/mlflow-model-local-inference-test.ipynb)

**OPTION B (LAST RESORT): Manual and low level model training with PyTorch, etc.**

In case Azure AutoML training was “too generic” for fire detection, these are other alternatives to evaluate (transfer learning performed on a more 'low level’ way):

Examples:

https://pyimagesearch.com/2019/11/18/fire-and-smoke-detection-with-keras-and-deep-learning/
https://ieeexplore.ieee.org/document/10205560
https://www.sciencedirect.com/science/article/pii/S2214157X2030085X?via%3Dihub
https://fireecology.springeropen.com/articles/10.1186/s42408-022-00165-0 

**Hackers assigned for this task (Using Jupyter notebook, Python and AML SDK):**
- CESAR DE LA TORRE


#### Create a Labeled fire/smoke images Dataset (For Object Detection)

- **OPTION A: Find an existing “fire/smoke" labeled dataset compatible with AutoML models (JSONL format)**
If the found training data is in a different format (like, pascal VOC or COCO), we can apply the helper scripts included with the sample notebooks to convert the data to JSONL. Learn more about [How to prepare data for computer vision tasks with automated ML](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-prepare-datasets-for-automl-images?view=azureml-api-2).

*Note: The training data needs to have at least 10 images in order to be able to submit an AutoML job.*

- **OPTION B: Use Azure ML Labeling for creating our own “fire/smoke" labeled dataset**

  https://learn.microsoft.com/en-us/azure/machine-learning/how-to-create-image-labeling-projects?view=azureml-api-2 

**Hackers assigned for this task (Images Dataset research OR dataset creation):**
- CESAR DE LA TORRE
- Frank Bruno
- Reza Etemadi

## Guidelines for Dev tasks

### Python: Integrate AI Model within the AI.Inference Python microservice  

Research the code from the "ai_inferencer" microservice in Python so instead of running the current "plain vanilla" YOLO model, it'll run our model for detecting fire/smoke.

https://github.com/CESARDELATORRE/wildfire-app-solution-accelerator/tree/main/src/Services/Detections/ai_inferencer

Additional information about the end to end solution is available at the ["MEC Application Solution Accelerator" architecture WORD document](https://github.com/CESARDELATORRE/wildfire-app-solution-accelerator/blob/main/docs/Architecture%20and%20Design%20of%20MEC%20Solution%20Accelerator.docx).

About how to locally (Python Docker container) inference a model that was created with AutoML, research this notebook:
*For inference with the model and make predictions (Developers / ML Engineer):*

[Inference model locally with MLFlow](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/automl-standalone-jobs/automl-image-object-detection-task-fridge-items/mlflow-model-local-inference-test.ipynb)

Basically, a similar Python code will need to run within the Python code "ai_inferencer" microservice in a Docker container. 

*TIP:* Get started with any example Object Detection model created by AutoML so we can start integrating it in the Solution's Python microservice, so when the final AutoML model is ready, it'll be quick to integrate/deploy it, since it'll be a very similar model from a deployment and inference point of view.

**Hackers assigned for this task (Python development):**
- CESAR DE LA TORRE
- Reza Etemadi
- Carsten Avenhaus

### Python: Create a fire/smoke "inference test video" and publish is as a Docker container  

This is a very simple development task. In order to simulate a video camera sending the video for fire and smoke detection, we need to assemble/create a test video with raw images (not labeled) with landscape, forest, and quite a few images with fire and smoke in it.

This video is what will be tested and working on the final application at the edge.

Once we have that video created (i.e. a .MP4 video), we will wrap it within a Docker container that will publish is as an RTSP url, like if it was a real IP camera with a RTSP url. 
This development is already donde and just needs to be updated with the new video. Check it out here:

https://github.com/CESARDELATORRE/wildfire-app-solution-accelerator/tree/main/rtsp-video-streamer-container

**Hacker assigned for this task (Python development):**
- CESAR DE LA TORRE

### .NET C#: Create custom “Alert Rules” specific for the “wildfire domain” in the "Alert Rules" C# microservice.

Research the code from the "Alerts.RuleEngine" microservice to create new Alerts and new Rules in YAML and C#.

https://github.com/CESARDELATORRE/wildfire-app-solution-accelerator/tree/main/src/Services/Alerts/RulesEngine

Additional information about how to create rules and alerts in the ["MEC Application Solution Accelerator" architecture WORD document](https://github.com/CESARDELATORRE/wildfire-app-solution-accelerator/blob/main/docs/Architecture%20and%20Design%20of%20MEC%20Solution%20Accelerator.docx)

**Hackers assigned for this task (C# development):**
- Stefan Saramet
- CESAR DE LA TORRE


## Create the story video of our Hackathon project

- Create the "Story narrative"
- Record interviews to the members of the project
- Edit video and create the final "Project story video" to be provided as our deliverable of the Hackathon.

*TIP:* Include pontential ideas in the story (even when not implemented in the hackathon) such as ability to tag "enemy/fire" here.
For instance, not just detecting fire/smoke but also sending back the related world-map coordinates coming from drones or robots. Those coordinates could be integrated into solutions such as TAK or [PyTAK](https://pytak.readthedocs.io/en/latest/), providing awareness to firefighters.

That would be very useful for firefighters in order to quickly go to the issue's area.

**Hackers assigned for this tasks:**
- Josh Waagmeester
- Joram Borenstein
- Frank Bruno
