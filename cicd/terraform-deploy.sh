#!/bin/bash

# fail on any error
set -eu

cd ..

echo "Going into infra backend"
cd infrastructure/backend 

echo "init deployment env for frontend"
terraform init

echo "Deploying backend infra & apps, outputing DNS Name to .env"
terraform apply --auto-approve

echo "Going into services frontend"
cd ../../services/frontend 
echo "Building fe image"

#This is to pass ALB DNS Name to FE Image, it can only be done in image build time for react
docker build  -t "tracktrace_repo:fe" --file "Dockerfile-prod" --build-arg REACT_APP_API_ENDPOINT=$(cat .env | xargs) --no-cache .
docker tag "tracktrace_repo:fe" "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:fe"
docker push "283879969377.dkr.ecr.ap-southeast-1.amazonaws.com/tracktrace_repo:fe"

echo "Going into infra frontend"
cd ../../infrastructure/frontend 

echo "init deployment env for frontend"
terraform init

echo "Deploying frontend"
terraform apply --auto-approve

echo "Done"