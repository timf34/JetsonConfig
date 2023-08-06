#!/bin/bash

# Define the environment variable and its value
ENV_VAR_NAME="DEVICE_NAME"
ENV_VAR_VALUE="jetson1"  # replace this with the desired device name

# Add the environment variable to /etc/environment
echo "$ENV_VAR_NAME=\"$ENV_VAR_VALUE\"" | sudo tee -a /etc/environment

# Export the variable in the current shell
export $ENV_VAR_NAME=$ENV_VAR_VALUE

echo "Environment variable $ENV_VAR_NAME added successfully."

# Print the value of the environment variable
echo "$ENV_VAR_NAME = $DEVICE_NAME"
