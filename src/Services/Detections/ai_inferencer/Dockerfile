# Use base Python image from Docker Hub and install required packages later
FROM python:3.8.16-slim-bullseye

# (CDLTLL) We could use the curated AutoML Training Docker image, but it's huge.. 22 GB.
# FROM mcr.microsoft.com/azureml/curated/azureml-automl-dnn-vision-gpu:121

# Copy requirements_app.txt
COPY requirements-app.txt ./

# Requirements for original Docker image without AutoML
RUN pip3 install --upgrade pip

RUN pip3 install -r requirements-app.txt
RUN pip3 uninstall opencv-python opencv-python-headless -y
RUN pip3 install opencv-python-headless

RUN apt-get update && apt-get -y install gcc cython3
RUN pip install cython
RUN pip install pycocotools==2.0.6

# Install requirements for AutoML Model
# (CDLTLL) Note that the requirements.txt file was modified/optimized. 
# The original /mlflow-model/requirements.txt had issues/errors 
# when trying to create the image with this Dockerfile. We updated some packages versions
# See PR: https://github.com/CESARDELATORRE/wildfire-app-solution-accelerator/pull/4
COPY ./mlflow-model/requirements.txt ./mlflow-model/
RUN pip3 install -r ./mlflow-model/requirements.txt

COPY . .

CMD python3 invoke-sender-frames.py