# Bottlenose Dolphins' Worldgate Track & Trace System

### Backend: Provide Database Connection String

This backend application relies on a remote Oracle server for data persistence.
Add db Connection String in ```docker-compose.yml``` (without quotes):

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



### Scrapers: Change arch to install the correct browser and driver

In ```./services/scrapers/Dockerfile-<Shipping Line>```
Change ```ARG ARCH``` to ```arm64``` or ```amd64```

### Running Containers

1. ```docker-compose build``` 
2. ```docker-compose up```