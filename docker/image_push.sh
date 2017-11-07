#! /bin/bash

IMAGE_NAME=$1
TAG=$2

echo "Image to be uploaded: '$IMAGE_NAME:$TAG'"

echo "Logging into AWS ECR"
$(aws ecr get-login --no-include-email --region us-east-1)

echo "Tagging $IMAGE_NAME:$TAG..."
docker tag $IMAGE_NAME:$TAG 626226570674.dkr.ecr.us-east-1.amazonaws.com/$IMAGE_NAME:$TAG 

echo "Pushing $IMAGE_NAME:$TAG to ECR"
docker push 626226570674.dkr.ecr.us-east-1.amazonaws.com/$IMAGE_NAME:$TAG

echo "DONE"
