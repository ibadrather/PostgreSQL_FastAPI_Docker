## PostgresSQL with Python FastAPI

I am learning how to use FastAPI with PostgresSQL. 

## Steps

1. Download and install PostgresSQL and setup Docker

2. Download Postgres Image from Docker Hub
   
    `docker pull postgres:alpine`

3. Create a container from the image

    `docker run --name fastapi-postgres -d -e POSTGRES_PASSWORD=postgres -d -p 8080:8080 postgres:alpine`

4. See if the container is running

    `docker ps`

5. Create a database in the container using psql
```bash
    # Enter the container
    docker exec -it fastapi-postgres bash

    # Enter psql
    psql -U postgres

    # Create a database
    CREATE DATABASE fastapi_database;

    # Create a user
    create user myuser with encrypted password 'mypass';

    # Grant privileges to the user
    grant all privileges on database fastapi_database to myuser;

    # go to the database
    \c fastapi_database
        output: You are now connected to database "fastapi_database" as user "postgres".
        fastapi_database=#

```

6. Right now it is accesible inside the container, but we want to access it from outside the container:

```bash
    psql -h localhost -p 8080 -U postgres
```

Now, it should be available from outside the container.


## Install dependencies

```bash
    pip3 install "fastapi[all]" sqlalchemy psycopg2-binary
```
