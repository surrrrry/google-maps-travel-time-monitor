#!/usr/bin/env bash

IMAGE_NAME=templateserviceimagename
docker rm -f $IMAGE_NAME || true
docker rmi -f $IMAGE_NAME ||  true
sh build-image.sh

docker run -dit -v /dev/shm:/dev/shm --name $IMAGE_NAME --net=host --restart always $IMAGE_NAME:latest
rm secrets.json
rm build-image.sh
rm Dockerfile
rm -r app