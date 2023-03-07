#!/bin/bash

# fail on any error
set -eu

cd ..

echo "Going into infra backend"
cd infrastructure/backend 

echo "init deployment env for frontend"
terraform init

echo "Deploying backend infra & apps, outputing DNS Name to .env"
terraform destroy --auto-approve

echo "Going into infra frontend"
cd ../frontend

echo "init deployment env for frontend"
terraform init

echo "Deploying frontend"
terraform destroy --auto-approve