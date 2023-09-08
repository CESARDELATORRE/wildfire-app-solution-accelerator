<p align="center">
  <img src="https://github.com/CESARDELATORRE/wildfire-app-solution-accelerator/assets/1712635/a36f8347-95af-453d-bb1e-a12540598827" alt="Wildfire accelerator logo"/>
  <img src="https://github.com/CESARDELATORRE/wildfire-app-solution-accelerator/assets/1712635/e2e4c5ea-fde9-43f2-b9be-bcaa52218b4d" alt="MSFT First Responders logo"/>
</p>

# Wildfire MEC/Edge Application Solution Accelerator

As part of the Microsoft Global Hackathon 2023, we want to make a difference and create value/assets around “wildfire detection” based on AI models detecting fire and smoke and generating alerts. 

# Problem or Opportunity (Story / End to end vision)

As we continue to face an ever-changing climate, we are starting to see increasing concerns around wildfires. These wildfires are difficult to control and detect. With this hackathon we are going to train an AI model to detect Fire and Smoke to be trained with a labeled dataset and to create rules to generate alerts that would allow take action on these detections. This model can be used across endless scenarios.

This solution can work reading data from any live video feeds (RTSPs) from static cameras in poles, drones, robots, Vehicle Fires from stationary traffic cameras, or any kind of connected IP cameras that could be installed inside of our national os state parks.

The following is an illustration of the end to end story and vision. 

![image](https://github.com/CESARDELATORRE/wildfire-app-solution-accelerator/assets/1712635/72b2dadb-798c-446c-abb5-25773425aa3d)

## Not in scope

In this hackathon's project, however, we won't directly deal with drones/robots and satellites but we suppose we can get video streaming from *any* source (Any RTSP). Therefore, the focus for this current project is on the 'Edge compute' and 'AI model' for detecting fire and smoke.

# Development goals

We will be building this solution based on the ["MEC Application Solution Accelerator”](https://github.com/Azure/mec-app-solution-accelerator) (Open Source code from our MSFT team), which provides the foundation for comparable scenarios for video analytics.

The core of this project is to create an AI Model for detecting fire & smoke and deploy it as part of the ["MEC Application Solution Accelerator”](https://github.com/Azure/mec-app-solution-accelerator) so it can work on an end to end solution consuming videos from any RTSP url (like from drones, robots, etc.) 

![image](https://github.com/CESARDELATORRE/wildfire-app-solution-accelerator/assets/1712635/83f19ee2-60ae-42df-80f9-81ac68f62ff4)

# Sub-Teams

- **AI/ML team:** AI model training and dataset labeling.
- **Dev team:** Model inference integration in Docker container. Alert rules implementation, etc.
- **Story telling and media team:** Story narrative, interviews to the team and video editing.

** TBD - NEED GitHub user accounts for each member in the hackathon project team **


# Main tasks

| | |
|--------|--------|
| **1. AI/ML motion** | - 1.1 Find or create a Labeled fire/smoke images Dataset (For Object Detection) - 1.2 Create/Train AI Model for detecting fire & smoke |
| **2. Dev motion** | - 2.1 Integrate AI Model within the AI.Inference Python microservice - 2.2 Create custom “Alert Rules” specific for the “wildfire domain” |
| **3. Story motion**| - 3.1 Create the "Story narrative" - 3.2 Record interviews to the members of the project - 3.3 Edit video and create the final "Project story video" to be provided as our deliverable of the Hackathon.|

## Guidelines for AI/ML tasks

### Create AI Model for detecting fire & smoke 

#### Train a new Object Detection model for detecting fire and smoke classes. Possible approaches:

    - Azure Machine Learning AutoML for computer vision models: AutoML automatically does transfer learning from these foundation object detection models: YOLOv5, ResNet, RetinaNet (multiple trainings trying these foundation models with different hyperparameter combinations)

      AutoML computer vision Tutorials: 
      
      https://learn.microsoft.com/en-us/azure/machine-learning/how-to-auto-train-image-models?view=azureml-api-2&tabs=cli   
      
      https://learn.microsoft.com/en-us/azure/machine-learning/how-to-use-automl-small-object-detect?view=azureml-api-2&tabs=CLI-v2 

    - Custom / low level training with PyTorch, etc.

**Hackers assigned for this task (Using Jupyter notebook, Python and AML SDK):**
- HACKER 1
- HACKER 2
- HACKER 3

#### Create a Labeled fire/smoke images Dataset (For Object Detection)

    - OPTION A: Find an existing “fire/smoke" labeled dataset compatible with AutoML models (JSONL format)

    - OPTION B: Use Azure ML Labeling for creating our own “fire/smoke" labeled dataset

        https://learn.microsoft.com/en-us/azure/machine-learning/how-to-create-image-labeling-projects?view=azureml-api-2 

**Hackers assigned for this task (Images Dataset research OR dataset creation):**
- HACKER 1
- HACKER 2
- HACKER 3

## Guidelines for Dev tasks

### Python: Integrate AI Model within the AI.Inference Python microservice  

Research the code from the "ai_inferencer" microservice in Python so instead of running the current "plain vanilla" YOLO model, it'll run our model for detecting fire/smoke.

https://github.com/CESARDELATORRE/wildfire-app-solution-accelerator/tree/main/src/Services/Detections/ai_inferencer

Additional information about the end to end solution is available at the "MEC Application Solution Accelerator" architecture document, here:

*********** TBD URL to ARCH DOC **************

**Hackers assigned for this task (Python development):**
- HACKER 1
- HACKER 2
- HACKER 3

### .NET C#: Create custom “Alert Rules” specific for the “wildfire domain” in the "Alert Rules" C# microservice.

Research the code from the "Alerts.RuleEngine" microservice to create new Alerts and new Rules in YAML and C#.

https://github.com/CESARDELATORRE/wildfire-app-solution-accelerator/tree/main/src/Services/Alerts/RulesEngine

Additional information about how to create rules and alerts in the "MEC Application Solution Accelerator" architecture document, here:

*********** TBD URL to ARCH DOC **************

**Hackers assigned for this task (C# development):**
- HACKER 1
- HACKER 2
- HACKER 3


### Create the story video of our Hackathon project

- Create the "Story narrative"
- Record interviews to the members of the project
- Edit video and create the final "Project story video" to be provided as our deliverable of the Hackathon.

**Hackers assigned for this tasks:**
- HACKER 1
- HACKER 2
- HACKER 3

# Getting Started

## Grab the GitHub repo code

Get the GitHub repo's code:

```powershell
git clone git@github.com:CESARDELATORRE/wildfire-app-solution-accelerator.git
```

## Local Docker deployment alternatives (Development and Test environment)

When developing, testing and debugging the MEC application it's easier and more straightforward to deploy into Docker so, for instance, you can debug code with Visual Studio and can easily test the application with just Docker installed without further setup steps as required by Kubernetes.

| | |
|--------|--------|
| <img width="140" alt="image" src="https://user-images.githubusercontent.com/1712635/220490921-dc521a14-3f0a-481f-8179-7233a744dbc1.png"> | **Deploy application services to [Docker for Desktop with 'docker compose up'](./docs/DOCKER_COMPOSE_DEPLOYMENT.MD)** |
| <img width="130" alt="image" src="https://user-images.githubusercontent.com/1712635/220490972-9140e540-3000-47f0-a3c4-4e64b4976266.png"> | **Deploy application services to Docker with [Visual Studio (F5 experience)](./docs/VS_DOCKER_DEPLOYMENT.MD)** |
| | |


## Kubernetes deployment alternatives ("Production" environment)

**IMPORTANT NOTE: The deployment to KUBERNETES below is related to the MEC Solution Accelerator. For the WILDFIRE ACCELERATOS we will need to change the instructions below when we change the Docker Images names for the AImodel.Infererence microservice and the Alerts-Rules microservice**

This sample microservices application can be deployed on most Kubernetes distributions clusters. 

Because we're targeting deployment at the Edge and also development environments, in most cases (unless you need significant process power when scaling out to many video sources/cameras) your Kubernetes clusters will be composed by a single cluster node (like a dev machine environment or light edge environment). 

Refer to the following procedure information pages to learn how to deploy this example application to your selected Kubernetes distribution:

| | |
|--------|--------|
| <img width="250" alt="image" src="https://user-images.githubusercontent.com/1712635/220757242-ee4bc4dc-2e70-4718-bcd6-12a800f84669.png"> | **Deploy application services to [local AKS Edge Essentials](/docs/K8S_AKS_EDGE_ESSENTIALS.MD)** |
| <img width="270" alt="image" src="https://user-images.githubusercontent.com/1712635/220753221-9bcbaf08-8de8-4064-a1ca-3b78e2dceff4.png"> | **Deploy application services to [local Kubernetes in 'Docker Desktop'](/docs/K8S_IN_DOCKER_DESKTOP_DEPLOYMENT.MD)** |
| <img width="200" alt="image" src="https://user-images.githubusercontent.com/1712635/220753664-79e9c307-54b8-40d3-8702-9b1d64349284.png"> | **Deploy application services to [local MiniKube](/docs/K8S_MINIKUBE_DEPLOYMENT.MD)** |
| <img width="190" alt="image" src="https://user-images.githubusercontent.com/1712635/220753942-2d66681c-8560-43bb-9ffc-85a787356549.png"> | **Deploy application services to [Azure Kubernetes Services](/docs/K8S_AKS_DEPLOYMENT.md)** in Azure cloud (Testing in the cloud) |
| | |

# Configurations for easy customization

In order to test your own scenarios you might want to try the following operations even before customizing or forking the application's code:

| | |
|--------|--------|
| <img width="70" alt="Camera icon" src="https://user-images.githubusercontent.com/1712635/220493758-47ec3c24-7a29-4e85-8f20-ee141e2f538a.png"> | **[How to provision your own video RTSP feed in the app with configuration](/docs/HOW_TO_PROVISION_NEW_FEED.MD)** |
| <img width="140" alt="image" src="https://user-images.githubusercontent.com/1712635/220490921-dc521a14-3f0a-481f-8179-7233a744dbc1.png"> | **[How to create a container with RTSP simulating a camera](/rtsp-video-streamer-container/)** |

 
