## PostgresSQL with Python FastAPI

This documentation provides a step-by-step guide on setting up a PostgreSQL database with Python FastAPI using Docker containers. It also covers the usage of SQLAlchemy and Alembic for database management and migrations.

### Requirements
Make sure you have the following dependencies installed on your system:
* Docker
* Docker Compose
* Python 3.9
* FastAPI
* SQLAlchemy
* Alembic


### Build Process
Follow these steps to build the application:
1. Create a `compose.yaml` file that defines three services:
   * `database`: PostgreSQL database service
   * `pgadmin`: pgAdmin service for database management
   * `app`: FastAPI application service

2. Create a `Dockerfile` for the `app` service. This file should include the necessary configurations to build the application image.

3. Create a `requirements.txt` file for the `app` service. This file should list all the Python dependencies required by the FastAPI application.

### How to Run
To run the application, execute the following commands:

```bash
docker compose build
docker compose up
```

or simply run the following command:
```bash
docker compose up --build
```

If you want to run the containers in the background in detached mode, you can use the `-d` flag:
```bash
docker compose up --build -d
```

This will build the Docker images and start the containers for the PostgreSQL database, pgAdmin, and the FastAPI application

It should look like this in the Docker Desktop application:

![Containers running](pictures/containers_running.png)


### Database Migrations with Alembic

1. Initialize Alembic by running the following command:
```bash
    alembic init alembic
```
This command will create a folder named `alembic` with an `alembic.ini` file and a `versions` folder.

1. Edit the `env.py` file to load environment variables from the `.env` file into the `.ini` file. Perform the following steps:
   * Add the path to the `.env` file in the `env.py` file.
   * Set the `sqlalchemy.url` value to the `DATABASE_URL` environment variable.
   * Import the models so that they are available for Alembic to create the migrations.
   * Add the following code to the `env.py` file:
  ```python
    import os
    import sys
    from dotenv import load_dotenv

    # Add the parent directory to the path so that we can import models.py
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    APP_PATH = os.path.join(BASE_PATH, "app")
    sys.path.append(BASE_PATH)
    sys.path.append(APP_PATH)

    # Load the environment variables
    load_dotenv()

    # this is the Alembic Config object, which provides
    # access to the values within the .ini file in use.
    config = context.config

    # Get the database URL from the environment variable
    config.set_main_option("sqlalchemy.url", os.environ["DATABASE_URL"])

    # Import the models so that they are available for Alembic to create the migrations
    import app.models

    target_metadata = app.models.Base.metadata

  ```

### Performing Migrations
Ensure that the database container is running, and then execute the following command:
```bash
    docker compose run app alembic revision --autogenerate -m "initial"
```

Finally, execute the following command to apply the migration to the database:
```bash
    docker compose run app alembic upgrade head
```

This command will generate an initial migration script based on the changes detected in the models defined in the `app` directory.

### NOTE:
This also includes the creation of a FastAPI backend application that will use data schemas for defining data models. These data schemas will serve two main purposes:

1. **Data Validation**: The schemas will verify and validate the data that is sent to various API endpoints. This ensures that the data being received is in the correct format and contains the necessary fields.

2. **Data Serialization**: The schemas will be used for serializing the data that is returned from the API endpoints. This means that the data will be converted into a format that is easier to read or transmit.

The data schemas will be defined within the `app/schemas.py` file. With these schemas, we can ensure that the data being processed is always in the correct format before it's stored within the database. This practice greatly reduces the chances of errors and inconsistencies in the data.

### Alternative Method (not recommended)

There is a setup.sh file that can be used to run the application. This file will build the Docker images and start the containers for the PostgreSQL database, pgAdmin, and the FastAPI application. It will also initialize Alembic and perform the database migrations.

To run the application using the `setup.sh` file, execute the following command:
```bash
    chmod +x setup.sh && ./setup.sh
```