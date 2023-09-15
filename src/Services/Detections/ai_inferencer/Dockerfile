FROM mcr.microsoft.com/azureml/curated/azureml-automl-dnn-vision-gpu:121
# FROM python:3.8.16-slim-bullseye

# Copy requirements.txt and conda.yaml files to the container
COPY requirements.txt ./

# Requirements for original Docker image without AutoML
RUN pip3 install --upgrade pip

# RUN pip3 install torch==1.13.1+cpu torchvision==0.14.1+cpu --extra-index-url https://download.pytorch.org/whl/cpu

RUN pip3 install -r requirements.txt
RUN pip3 uninstall opencv-python opencv-python-headless -y
RUN pip3 install opencv-python-headless

## Install required packages
#RUN apt-get update && \
#    apt-get install -y wget bzip2 && \
#    rm -rf /var/lib/apt/lists/*

## Download and install Miniconda
#RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
#    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
#    rm Miniconda3-latest-Linux-x86_64.sh

## Add conda to PATH
#ENV PATH /opt/conda/bin:$PATH

## Verify that conda is installed
#RUN conda --version

## Create conda environment
#COPY ./mlflow-model/conda.yaml ./

#RUN conda env create --file ./conda.yaml

## Activate conda environment
# RUN echo "conda activate project_environment" > ~/.bashrc

# ENV PATH /opt/conda/envs/project_environment/bin:$PATH

COPY . .

CMD python3 invoke-sender-frames.py