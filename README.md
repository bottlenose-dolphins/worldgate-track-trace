# Bottlenose Dolphins' Worldgate Track & Trace System

### Backend: Provide Database Connection String

This backend application relies on a remote Oracle server for data persistence.
While it is possible to add db Connection String via a Dockerfile:

In ``` ./services/backend/Dockerfile```,
Add db connection string to ```ENV SQLALCHEMY_DATABASE_URI=```

It may be safer to utilise a ```.env``` file, given it will not be committed.
[Docker will automatically retrieve env variables when using ```docker-compose```](https://docs.docker.com/compose/environment-variables/#:~:text=The%20.env%20file%20feature%20only). [Note that this does not seem to be the case when running specific dockerfiles, i.e. using ```docker build```](https://vsupalov.com/docker-arg-env-variable-guide/). Therefore, when testing individual containers, kindly do the aforementioned. 

In most cases, as previously, edit the `.env-example` using any text editor (`vi .env.example`).

1. Replace `<>` fields with the respective information
2. Rename `.env.example` to `.env`

```bash
# Clone into a .env file
PYTHONPATH="${PYTHONPATH}:." # DO NOT CHANGE THIS
SQLALCHEMY_DATABASE_URI=<DB URI>

```

### Scrapers: Change arch to install the correct browser and driver

In ```./services/scrapers/Dockerfile-<Shipping Line>```
Change ```ARG ARCH``` to ```arm64``` or ```amd64```

### Running Containers

1. ```docker-compose build``` 
2. ```docker-compose up```