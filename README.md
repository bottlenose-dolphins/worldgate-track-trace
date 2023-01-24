# Bottlenose Dolphins' Worldgate Track & Trace System

### Backend: Provide Database Connection String + Installing the correct Oracle Client library 

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
Add db connection string to ```ENV SQLALCHEMY_DATABASE_URI=<DB URI```


2. Comment out irrelevant Oracle Client Library Download in ```./services/backend/Dockerfile```


```
            #for ARM
            && wget https://download.oracle.com/otn_software/linux/instantclient/191000/instantclient-basiclite-linux.arm64-19.10.0.0.0dbru.zip \
            && unzip instantclient-basiclite-linux.arm64-19.10.0.0.0dbru.zip \
            && rm -f instantclient-basiclite-linux.arm64-19.10.0.0.0dbru.zip \

            #for AMD86
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