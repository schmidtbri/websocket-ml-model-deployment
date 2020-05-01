# Websocket ML Model Deployment


![Test and Build](https://github.com/schmidtbri/websocket-ml-model-deployment/workflows/Test%20and%20Build/badge.svg?branch=master&event=push) 
![Build Docker](https://github.com/schmidtbri/websocket-ml-model-deployment/workflows/Build%20Docker/badge.svg?branch=master&event=release)

Deploying an ML model in a websocket service.

This code is used in this [blog post](https://medium.com/@brianschmidt_78145/a-websocket-ml-model-deployment-22d73938541b).

## Requirements
Docker

## Installation 
The makefile included with this project contains targets that help to automate several tasks.

To download the source code execute this command:

```bash
git clone https://github.com/schmidtbri/websocket-ml-model-deployment
```

Then create a virtual environment and activate it:

```bash
# go into the project directory
cd websocket-ml-model-deployment

make venv

source venv/bin/activate
```

Install the dependencies:

```bash
make dependencies
```

Start the development server:
```bash
make start-server
```

Test the development server with some requests:
```bash
make test-models-endpoint

make test-metadata-endpoint

make test-predict-endpoint
```

## Running the Unit Tests
To run the unit test suite execute these commands:
```bash
# first install the test dependencies
make test-dependencies

# run the test suite
make test
```

## Running the Service
To run the service, run these commands:

```bash
export PYTHONPATH=./
export APP_SETTINGS=ProdConfig
gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:80 model_websocket_service:app
```

## Docker
To build a docker image for the service, run this command:
```bash
docker build -t model-websocket-service:latest .
```

To run the image, execute this command:
```bash
docker run -d -p 80:80 --env APP_SETTINGS=ProdConfig model-websocket-service
```

To watch the logs coming from the image, execute this command:
```bash
docker logs $(docker ps -lq)
```

To get the latest build of this image from Dockerhub, execute this command:

```bash
docker pull bschmidt135/websocket-ml-model-deployment
```
