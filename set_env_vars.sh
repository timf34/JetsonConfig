#!/bin/bash

# Define the environment variable and its value
ENV_VAR_NAME="DEVICE_NAME"
ENV_VAR_VALUE="jetson1"  # replace this with the desired device name

# Check if the environment variable is already in /etc/environment
if grep -q "$ENV_VAR_NAME" /etc/environment; then
    echo "Environment variable $ENV_VAR_NAME already exists."
else
    # Add the environment variable to /etc/environment
    echo "$ENV_VAR_NAME=\"$ENV_VAR_VALUE\"" | sudo tee -a /etc/environment

    # Reload /etc/environment to make the new variable available immediately
    source /etc/environment

    echo "Environment variable $ENV_VAR_NAME added successfully."
fi

# Print the value of the environment variable
echo "$ENV_VAR_NAME = $DEVICE_NAME"
