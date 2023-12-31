# Deployment to Kubernetes in 'Docker Desktop'

Docker Desktop includes a [standalone Kubernetes](https://docs.docker.com/desktop/kubernetes/) server and client, as well as Docker CLI integration that runs on your machine.

The Kubernetes server runs locally within your Docker instance, is not configurable, and is a single-node cluster. It runs within a Docker container on your local system, and is only for local testing.

## Install/enable Kuberentes in Docker Desktop

Make sure you have installed ["Docker Desktop"](https://docs.docker.com/desktop/install/windows-install/).

Once you have installed Docker Desktop, enable Kubernetes by following these instructions.

### Enable Kubernetes in Docker Desktop

1. In order to Enable Kubernetes in Docker Desktop, check out the instructions from Docker:

    - [Enable Kuberentes in Docker Desktop](https://docs.docker.com/desktop/kubernetes/)

2. If you previosly had already installed kubectl and it is pointing to some other environment, such as MiniKube, make sure the default kubectl context is pointing to docker-desktop. 

    Open a new command-shell and run the following command to check your current contexts:

    ```powershell
    kubectl config get-contexts
    ```

    To set the context to point to Kuberentes from Docker Desktop:

    ```powershell
    kubectl config use-context docker-desktop
    ```
    
    ![image](https://user-images.githubusercontent.com/1712635/218879865-f41a5a72-0f8e-4fc2-8d40-5543ce455942.png)

## (Optional) Instructions for building your own Docker Images to deploy to Kubernetes

You can directly deploy to Kubernetes and test the images we have already uploaded into Docker Hub, so creating your own Docker images and uploading to Docker Hub is optional, initially.

However, if you make changes in the code or you want to use your own Docker Images for any reason, you'd need to create your own Docker images and upload the images first to Docker Hub before deploying to Kubernetes. 

Use these instructions to [Buil your own Docker Images to upload to Docker Registry and deploy to Kubernetes](./BUILD_AND_PUSH_IMAGES_TO_DOCKER_HUB.MD)

## Deploy the Application to Kubernetes in 'Docker Desktop'

This example application is based on **[Dapr](https://dapr.io/)** framework which is an OSS Microsoft framework specialized on microservices architecture, so you need to install it and enable in the Kubernetes cluster, first. 

### Install and Initialize DAPR

3. Install or make sure you have installed `Dapr` on your machine on a Kubernetes cluster as described in the [Deploy dapr](https://docs.dapr.io/operations/hosting/kubernetes/kubernetes-deploy/#install-with-dapr-cli). 

Note that if you were able to run the application on plain Docker, you should have installed DAPR already, but it needs to be initialized in Kuberentes, now.

4. Initialize DAPR in the Kubernetes cluster by running this command:
5. 
    ```powershell
    dapr init -k
    ```
    
    ![image](https://user-images.githubusercontent.com/1712635/218881163-9ba81fa3-f72c-4c12-bbf6-8ec25f2dba55.png)

    **IMPORTANT:** This DAPR installation is okay for a dev machine, but when installing DAPR on a "production" AKS cluster, for example in an ASE (Azure Stack Edge) server, you need to install DAPR via AKS extension following the Doc: (https://learn.microsoft.com/en-us/azure/aks/dapr) which is how DAPR should be installed in AKS and it doesn’t require cluster admin access.
    
    You can test DAPR status with:
    ```powershell
    dapr status -k
    ```
    
    If DAPR is initialized, you should get this list of Dapr pods running:
    
    ![image](https://user-images.githubusercontent.com/1712635/218881242-aa2c74ef-14a4-4a79-a149-3bbd12f4fa3d.png)

    
    Otherwise, if it's not initialized it'd be like this:
    
    ![image](https://user-images.githubusercontent.com/1712635/218880976-94b42767-40e3-4d9c-a640-2dfa029cb510.png)

    
### Deploy the application's services to Kubernetes

5. Open a new command-shell and move into the `deploy/k8s` folder of this repo, as current folder of the command-shell:

    ```powershell
    cd <your_path>/deploy/k8s
    ```

6. Deploy the application in Kuberentes by running this command:

    ```powershell
    kubectl apply -f ./
    ```

    All services will be created in the specified Kubernetes namespace "mec-accelerator" for this application.
    
    ![image](https://user-images.githubusercontent.com/1712635/219480144-75f3998d-998c-464d-bc8a-7e9a1a265a0e.png)

    When you are finished trying, you can always uninstall the application pods and all related resources from your Kuberentes by running this command:

    ```powershell
    kubectl delete -f ./
    ```

### Check the application status with Kubernetes Dashboard

7. If you don't have installed/enabled the Kuberentes Dashboard, do so by running this command:

    ```powershell
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.6.1/aio/deploy/recommended.yaml
    ```

8. Run `kubectl proxy` so you can access the dahboard:

    ```powershell
    kubectl proxy
    ```
    
    ![image](https://user-images.githubusercontent.com/1712635/218886875-0f4f1c1f-1791-4bdb-93e0-cc3ab437750a.png)

    Kubectl will make Dashboard available at  
http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/

![image](https://user-images.githubusercontent.com/1712635/218886986-d838bc24-b103-437c-8f60-ebe5c2cc1095.png)

However, at this point you need to provide a security token to athenticate and enter the dashboard.
Let's do that in the following steps.

### Configure Bearer Tokens from Kuberentes to access the Dashboard

9. You need to do this step **only one time**: Change the current folder to the `deploy/k8s/dashboard_auth` folder of this repo and run the instructions in commands.txt to configure the tokens. Basically, the following commands need to be run just once from that folder:

    ```powershell
    kubectl apply -f dashboard-adminuser.yaml 

    kubectl apply -f adminuser-cluster-role-binding.yaml
    ```
    
    ![image](https://user-images.githubusercontent.com/1712635/218881848-92de552c-a0f3-4fa8-ab87-2ca2512956f2.png)


### Generate and copy the token to provide to Kubernetes Dashboard

10. Whenever you need a token, run this command:

    ```powershell
    kubectl -n kubernetes-dashboard create token admin-user --duration=48h --output yaml
    ```
    
    Select and copy the token to the clipboard.
    
    ![image](https://user-images.githubusercontent.com/1712635/218882035-61318473-b7e1-4fe5-b253-69479e8a20b0.png)

### Provide the token to Kubernetes dashboard

11. Open http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/login in your browser and paste the token you copied previously.

![image](https://user-images.githubusercontent.com/1712635/218882193-938f14f0-06ca-4bba-979f-da9266706f8e.png)

In the Kubernetes dashboard you should be able to explore the application's pods, services, etc.

![image](https://user-images.githubusercontent.com/1712635/219480986-86a6e67b-7fb8-41ea-8ca3-5948c1e5d358.png)


### Access the application's UI to see Alerts originated from AI model detections

12. To access the front-end, go to 'http://localhost/' on your browser or using the Kubernetes dashboard, select the Kuberentes namespace where the application is deployed, go to the services menu in the left tab and click on the url to the right on the UI service row.

![image](https://user-images.githubusercontent.com/1712635/218883329-5641f19c-f3d9-402f-a75e-2fe44aa6c9eb.png)

Either way, you should be able to run the application's UI and check out the Alerts originated from the AI models:

![image](https://user-images.githubusercontent.com/1712635/218885207-5d720a2d-f5a6-4e29-bfd1-bad384803805.png)

### Remove the application from Kubernetes 

1. Open a new command-shell and change the current folder to the `deploy/k8s` folder of this repo.

1. Run the following command to remove all related kubernetes resources for this application, since there is no stop action on kubectl.

    ```powershell
    kubectl delete -f ./
    ```




