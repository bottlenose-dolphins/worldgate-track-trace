# Bottlenose Dolphins' Worldgate Track & Trace System

### Setting up Cloud Infrastructure: AWS & Terraform

1. Obtain a secret key and configure with AWS

2. Configure AWS cli: https://docs.aws.amazon.com/cli/v1/userguide/install-linux.html: 

      1. run ```aws configure```
      2. insert access key, secret key, region: ```ap-southeast-1``` & output: ```json```

3. Setting up Terraform 

      1. change into the infrastructure dir
      2. run ```terraform init```
      3. run ```terraform plan``` to note the changes
      4. run ```terraform apply --auto-approve```

4. Taring down Terraform 

      1. run ```terraform-destroy --auto-approve```

### Development Backend: Provide Database Connection String + Installing the correct Oracle Client library 

This backend application relies on a remote Oracle server for data persistence.


1. Add db Connection String in ```docker-compose.yml``` (without quotes):

```
...

services:
  backend_users:
    container_name: backend_users
    build:
      context: ./services/backend
      dockerfile: Dockerfile
    environment:
      - SQLALCHEMY_DATABASE_URI=<DB URI>
    ports:
      - 5002:5002
```

When testing individual docker files, in ``` ./services/backend/Dockerfile```,
Add db connection string to ```ENV SQLALCHEMY_DATABASE_URI=<DB URI>```


2. Comment out irrelevant Oracle Client Library Download in ```./services/backend/Dockerfile```


```
#for ARM64
&& wget https://download.oracle.com/otn_software/linux/instantclient/191000/instantclient-basiclite-linux.arm64-19.10.0.0.0dbru.zip \
&& unzip instantclient-basiclite-linux.arm64-19.10.0.0.0dbru.zip \
&& rm -f instantclient-basiclite-linux.arm64-19.10.0.0.0dbru.zip \

#for X64
# && wget https://download.oracle.com/otn_software/linux/instantclient/219000/instantclient-basiclite-linux.x64-21.9.0.0.0dbru.zip \
# && unzip instantclient-basiclite-linux.x64-21.9.0.0.0dbru.zip \
# && rm -f instantclient-basiclite-linux.x64-21.9.0.0.0dbru.zip \
```

### Scrapers: Change arch to install the correct browser and driver

In ```./services/scrapers/Dockerfile-<Shipping Line>```
Change ```ARG ARCH``` to ```arm64``` or ```amd64```

### Running Containers

1. ```docker-compose build``` 
2. ```docker-compose up```


### Issues & Workarounds in Docker env:

1. Scrapers may fail through page crashes --> This is since the mem allocated to the docker container is insufficient. Read more [here](https://www.roelpeters.be/solve-selenium-error-session-deleted-because-of-page-crash/) 

Current Workaround: it is specified in the docker-compose file to allocate additional memory to 2 containers (at the time of writing, kmtc & onescraper). The other 2 scrapers (goodrich, ymlu work most of the time), if it crashes do give a reload.

2. Docker build fails sometimes, notably when```apt-get update``` is used, this has been seen & unresolved on windows machines at the time of writing. 

Current Workaround: We will dockerise Images into  ARM64\LINUX as well and push on to ECR whenever possible (At the time of writing, all non-scraper containers can be produced, though it has not been done)

3. Docker compose issues (upon upgrading to docker buildx with the new buildkit) --> this seems to be due to docker failing to move the build cache to build. When I build each image separately with ```docker build --load``` (load, helps to 'tag' the image, else there will be a warning, btw you may provide filename using ```-f <Dockerfile filename>```), and then running compose, no issues were faced, please let me know if you experience this as well