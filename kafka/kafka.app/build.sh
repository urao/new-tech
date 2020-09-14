#!/bin/bash
# Create ansible docker image with Junos ansible and jsnapy modules

echo "clean up old containers (if any)"
docker stop kafka_app
docker rm kafka_app

echo "Building new container"
docker build -t kafka_app --build-arg SCALA_VERSION=2.12 --build-arg KAFKA_VERSION=2.4.1 .

echo "Running new container in background"
docker run -d --name=kafka_app kafka_app 

echo "Output"
docker ps

exit 0
