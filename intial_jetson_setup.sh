#!/bin/bash

# Note: 
# Run this command before any of this to install imx477 driver (will need to follow commands and reboot)
# sudo /opt/nvidia/jetson-io/jetson-io.py


# cd into Desktop
cd ~/$USER/Desktop

# Check if FOVCamerasWebApp directory exists
if [ ! -d "FOVCamerasWebApp" ]; then
    # Clone the FOVCamerasWebApp repository
    git clone https://github.com/timf34/FOVCamerasWebApp.git
fi

# Check if JetsonWiFiManager directory exists
if [ ! -d "JetsonWiFiManager" ]; then
    # Clone the JetsonWiFiManager repository
    git clone https://github.com/timf34/JetsonWiFiManager.git
fi

# Install pip
sudo apt update
sudo apt install python3-pip -y

# Install FOVCamerasWebApp dependencies
cd ~/$USER/Desktop/FOVCamerasWebApp/jetson
pip3 install -r nano_requirements.txt

# Create a .env file 
touch .env
echo "REACT_APP_URL=http://localhost:5000" > .env  # For development
# echo "REACT_APP_URL=http://fovcameraswebappv2.eu-west-1.elasticbeanstalk.com" >> .env  # For production


# Install JetsonWiFiManager dependencies
cd ~/$USER/Desktop/JetsonWiFiManager
pip3 install -r requirements.txt
chmod +x install_packages.sh
./install_packages.sh
