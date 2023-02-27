# Bottlenose Dolphins' Worldgate Track & Trace System

### Environment Overview

Track&Trace is a multi-environment project, as such, some inconveniences may be experienced at the level you are working at to cater to users of other environments. 

##### Undockerised Development:

Those working on the backend may have to toggle between these in their ```.py``` files

```
if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5009, debug=True) #to be toggled on
    app.run(host='0.0.0.0', debug=True) #to be toggled off
```

##### Containerised Overview:

There are 2 dockerfiles for each microservice & also for the frontend . 
One labelled ```dev```, e.g. ```Dockerfile-dev``` and the other ```prod```. e.g. ```Dockerfile-prod```.

```dev``` dockerfiles are used in creating images, containers used when running in one's local machine

```prod``` dockerfiles are used in creating images, containers used when running externally

##### Local Containers:

Clone the ```.example-dev-env``` file and fill in the various credentials

In addition, comment out irrelevant Oracle Client Library Download in ```./services/backend/core```

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

This also needs to be done in ```./services/scrapers/Dockerfile-<Shipping Line>``` by Changing ```ARG ARCH``` to ```arm64``` or ```amd64```

Lastly, run ```docker compose``` in the root dir



*However, when running individual containers, you'll need to pass values into the dockerfile for e.g.

Add db connection string to ```ENV SQLALCHEMY_DATABASE_URI=<DB URI>```


##### Hosted Containers:

Track&Trace incorporates Infrastructure As Code through the use of Terraform which deploys the Infrastructure and hosts the relevant docker containers on AWS


This requires some set up:

1. Obtain an access key and secret from AWS 

2. Configure AWS cli: https://docs.aws.amazon.com/cli/v1/userguide/install-linux.html: 

      1. run ```aws configure```
      2. insert access key, secret key, region: ```ap-southeast-1``` & output: ```json```

3. Bring up environment with Terraform 

      1. Download Terraform cli
      2. Go into ```infrastructure/frontend```
      3. run ```terraform init```
      4. Go into ```infrastructure/frontend```
      5. run ```terraform init```
      6. From root dir, execute ```./terraformdeploy.sh```, you may have to run ```chmod +x terraformdeploy.sh```

4. Taring down Terraform 

      1. run ```terraform destroy --auto-approve``` in the ```infrastructure/frontend```
      2. run ```terraform destroy --auto-approve``` in the ```infrastructure/backend```
      *Note that ECR fail to destroy error is expected because existing docker images are still stored in ECR


### Issues & Workarounds for Docker:

1. Scrapers may fail through page crashes --> This is since the mem allocated to the docker container is insufficient. Read more [here](https://www.roelpeters.be/solve-selenium-error-session-deleted-because-of-page-crash/) 

Current Workaround: it is specified in the docker-compose file to allocate additional memory to 2 containers (at the time of writing, kmtc & onescraper), however, when running individual containers, you may do so like this:```docker run -p <host_port>:<container_port> --shm-size=800m <image_tag> ```
The other 2 scrapers (goodrich, ymlu work most of the time), if it crashes do give a reload.

2. Docker build fails sometimes, notably when```apt-get update```is used, this has been seen & unresolved on windows machines at the time of writing. 

Current Workaround: We will dockerise Images into  ARM64/LINUX as well and push on to ECR whenever possible (This is limited to all non-scraper microservices, though it has not been done)

[NOT IMPORTANT IF YOU ARE NOT USING DOCKER BUILDX]
3. Docker compose issues (upon upgrading to docker buildx with the new buildkit) --> this seems to be due to docker failing to move the build cache to build. When I build each image separately with ```docker build --load``` (load, helps to 'tag' the image, else there will be a warning, btw you may provide filename using ```-f <Dockerfile filename>```), and then running compose, no issues were faced, please let me know if you experience this as well
