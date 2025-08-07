#!/usr/bin/env bash

CURRENT_VERSION=latest
OWNER=surrrrry
IMAGE_NAME=googlemapstraveltimemonitor
MY_GIT_PAT=SPECIAL_TOKEN

docker build . --no-cache --build-arg GIT_PAT=$MY_GIT_PAT --build-arg SECRETS_FILE_PATH=secrets.json --tag $IMAGE_NAME:$CURRENT_VERSION
docker tag $IMAGE_NAME:$CURRENT_VERSION $IMAGE_NAME:latest
