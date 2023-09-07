# Wildfire MEC/Edge Application Solution Accelerator

As part of the Microsoft Global Hackathon 2023, we want to make a difference and create value/assets around “wildfire detection” based on AI models detecting fire and smoke and generating alerts. 

The following is an illustration of the end to end story and vision. In this hackathon's project, however, we won't deal with drones and satellites but suppose we can get video streaming from *any* source. Then, the focus for this current project is on the Edge compute and AI model for detecting fire and smoke.

![image](https://github.com/CESARDELATORRE/wildfire-app-solution-accelerator/assets/1712635/72b2dadb-798c-446c-abb5-25773425aa3d)

We will be building based on the ["MEC Application Solution Accelerator”](https://github.com/Azure/mec-app-solution-accelerator) (Open Source code from our MSFT team), which provides the foundation for comparable scenarios for video analytics.

# Problem or Opportunity

As we continue to face an ever-changing climate, we are starting to see increasing concerns around wildfires. These wildfires are difficult to control and detect. With this hackathon we are going to train an AI model to detect Fire and Smoke, create labels for this data set and to create rules to take action on these detections. This model can be used across endless scenarios.

This solution can be scoped and scaled to read data from live video feeds from Drones and robots, Vehicle Fires from stationary traffic cameras, or even cameras inside of our national parks.

## Main goal

Create an AI Model for detecting fire & smoke and deploy it as part of the ["MEC Application Solution Accelerator”](https://github.com/Azure/mec-app-solution-accelerator) so it can work on an end to end solution consuming videos from any RTSP url (like from drones, robots, etc.) 

![image](https://github.com/CESARDELATORRE/wildfire-app-solution-accelerator/assets/1712635/83f19ee2-60ae-42df-80f9-81ac68f62ff4)

## Main tasks
- Find or create a Labeled fire/smoke images Dataset (For Object Detection)
- Create AI Model for detecting fire & smoke
- Create custom “Alert Rules” specific for the “wildfire domain”

## Teams

- AI/ML team
- Video/Images team
- Devs/Application team
  
