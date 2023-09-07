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

## Teams

- **AI/ML team:** AI model training and dataset labeling.
- **Dev team:** Model inference integration in Docker container. Alert rules implementation, etc.
- **Story telling and media team:** Story narrative, interviews to the team and video editing.


## Main tasks
- Find or create a Labeled fire/smoke images Dataset (For Object Detection)
- Create AI Model for detecting fire & smoke
- Create custom “Alert Rules” specific for the “wildfire domain”


  
