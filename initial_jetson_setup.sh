#!/bin/bash

# Note: 
# Run this command before any of this to install imx477 driver (will need to follow commands and reboot)
# sudo /opt/nvidia/jetson-io/jetson-io.py

username=$USER

# cd into Desktop
# Note: you might need to just hardcode the paths here!
cd ~/Desktop

# Check if FOVCamerasWebApp directory exists
if [ ! -d "FOVCamerasWebApp" ]; then
    # Clone the FOVCamerasWebApp repository
    git clone https://github.com/timf34/FOVCamerasWebApp.git
    sudo chown -R $USER: FOVCamerasWebApp
fi

# Install pip
sudo apt update
sudo apt install python3-pip -y

# Some other packages 
sudo apt install nano
sudo apt install cmake
sudo apt install libssl-dev
sudo apt install network-manager


pip3 install -r requirements.txt

# Install FOVCamerasWebApp dependencies
cd ~/Desktop/FOVCamerasWebApp/jetson
pip3 install -r nano_requirements.txt

# Create a .env file 
touch .env
# echo "REACT_APP_URL=http://localhost:5000" > .env  # For development
echo "REACT_APP_URL=http://fovcameraswebappv2.eu-west-1.elasticbeanstalk.com" >> .env  # For production


# ------------------- Download and build aws-iot-device-client ----------------------------
cd ~/Desktop
git clone https://github.com/timf34/aws-iot-device-client
cd aws-iot-device-client
mkdir build
cd build
cmake ../
cmake --build . --target aws-iot-device-client

# Run the setup after this initial install script as we need to do so interactively as root 
# cd .. 
# sudo ./setup.sh

# ---------- Change permissions of the aws iot device certificates ------------ (assuming they've already been downloaded)
cd ~
chmod 700 aws-iot-certs/
cd aws-iot-certs
chmod 600 private.pem.key
chmod 644 certificate.pem.crt
chmod 644 AmazonRootCA1.pem

# ---------- Setup the git pull service ------------
cd ~/Desktop/JetsonConfig/git_pull_service
chmod +x git_pull.sh
chmod +x git_pull_setup.sh
./git_pull_setup.sh


# ----------- Setup the device shadow service ------------