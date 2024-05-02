# QR_generator:

This repository contains an example application used for testing the Segno library and local Kubernetes deployment using Minikube.

## Overview

The purpose of this project is to demonstrate how to integrate and test the Segno library in a real-world application, as well as how to deploy it locally using Minikube. Segno is a Python library for generating QR codes, and this example app showcases its usage within a larger project.

## Features

- Integration of Segno library for QR code generation with Flask app.
- Testing local deployment of the application using Minikube.


## Getting Started:


### Commands reminder:

#### To run on my configuration:

```powershell
docker context use default
docker-compose up -d --build
docker image save -o image.tar qr_generator-web:latest

minikube delete --all --purge
minikube start
minikube image load image.tar

kubectl apply -f .\qrgen-deploy.yaml
kubectl apply -f .\qrgen-service.yaml
kubectl apply -f .\ingress.yaml

minikube tunnel
```

#### Checks:

```powershell
kubectl get pods       
docker images
```

#### Default run:

http://127.0.0.1:5000/
