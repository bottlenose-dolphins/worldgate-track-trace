#!/bin/bash

# fail on any error
set -eu

cd ..

echo "Going into infra backend"
cd infrastructure/backend 

echo "init deployment env for backend"
terraform init

echo "Deploying backend infra & apps"
terraform apply --auto-approve

echo "Going into infra frontend"
cd ../frontend 

echo "init deployment env for frontend"
terraform init

echo "Deploying frontend"
terraform apply --auto-approve

echo "Done"