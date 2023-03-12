#!/bin/bash

# fail on any error
set -eu

cd ..

echo "Going into infra frontend"
cd infrastructure/frontend 

echo "init deployment env for frontend"
terraform init

echo "Deploying frontend infra & app"
terraform destroy --auto-approve

echo "Going into infra backend"
cd ../backend

echo "init deployment env for backend"
terraform init

echo "Deploying backend"
terraform destroy --auto-approve