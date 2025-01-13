#!/bin/bash

# Define variables
ZIP_FILE="<zip_file_name.zip>"
REPOSITORY="your.docker.repository.com" #basename of the repository
DOCKER_USER="your_docker_username" # docker, harbor or quay... it dos't mater
DOCKER_PASSWORD="your_docker_password"

# Unzip the file
unzip "$ZIP_FILE" -d getapp-images

# Iterate over each tar file
for TAR_FILE in images/*.tar; do
    # Load the image from the tar file
    docker load -i "$TAR_FILE"

    # Get the image ID
    IMAGE_ID=$(docker images --format "{{.ID}}" | head -n 1)

    # Tag the image
    docker tag "$IMAGE_ID" "$REPOSITORY/$(basename "$TAR_FILE" .tar)"

    # Log in to Docker Hub
    echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USER" --password-stdin "$REPOSITORY"

    # Push the image to the Docker repository
    docker push "$REPOSITORY/$(basename "$TAR_FILE" .tar)"

    # Clean up
    docker rmi "$IMAGE_ID"
    docker rmi "$REPOSITORY/$(basename "$TAR_FILE" .tar)"
done

# Clean up
rm -rf getapp-images
