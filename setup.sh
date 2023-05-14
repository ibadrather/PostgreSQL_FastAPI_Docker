#!/bin/bash

# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "Docker is not installed. Please install Docker and try again."
    exit
fi

# Check if Docker Compose is installed
if ! command -v docker compose &> /dev/null
then
    echo "Docker Compose is not installed. Please install Docker Compose and try again."
    exit
fi

# Build and run the Docker containers
echo "Building and running the Docker containers..."
docker compose up --build -d


# Run Alembic migrations
echo "Running Alembic migrations..."
docker compose run app alembic revision --autogenerate -m "initial"
docker compose run app alembic upgrade head

echo "Setup completed successfully!"
