# Running containers for Bottlenose Dolphins' Worldgate Track & Trace System

### Frontend: Add DB_URI

In ``` ./services/backend/Dockerfile```,
Add db connection string to ```SQLALCHEMY_DATABASE_URI```

### Scrapers: Change arch to install the correct browser and driver

In ```./services/scrapers/Dockerfile-<Shipping Line>```
Change ```ARG ARCH``` to ```arm64``` or ```amd64```

### Running Containers

1. ```docker-compose build```
2. ```docker-compose up```