#!/bin/bash

# Note: 
# Run this command before any of this to install imx477 driver (will need to follow commands and reboot)
# sudo /opt/nvidia/jetson-io/jetson-io.py

username=$USER

# Run this so github creds are remembered
git config --global credential.helper store

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
sudo apt update -y
sudo apt install python3-pip -y

# Some other packages 
sudo apt install -y nano
sudo apt install -y cmake
sudo apt install -y libssl-dev
sudo apt install -y network-manager
sudo apt install -y python3-gi
sudo apt install -y nvidia-tensorrt
sudo apt install -y arp-scan

cd ~/Desktop/JetsonConfig

pip3 install -r requirements.txt

# Install FOVCamerasWebApp dependencies
cd ~/Desktop/FOVCamerasWebApp/jetson
pip3 install -r nano_requirements.txt

# Install PyTorch
# Ensure that torchvision and torch are uninstalled
export TORCH_INSTALL=https://developer.download.nvidia.cn/compute/redist/jp/v511/pytorch/torch-2.0.0+nv23.05-cp38-cp38-linux_aarch64.whl
pip install --no-cache $TORCH_INSTALL
pip install torchvision==0.15.1

# Install TensorRT
sudo apt-get install libopenblas-base libopenmpi-dev libomp-dev -y
sudo apt-get install tensorrt nvidia-tensorrt-dev python3-libnvinfer-dev -y
pip install cuda-python

# Create a .env file 
touch .env
# echo "REACT_APP_URL=http://localhost:5000" > .env  # For development
# TODO: ensure the URL is correct!
echo "REACT_APP_URL=http://fovcameraswebappv2.ap-southeast-2.elasticbeanstalk.com/" >> .env  # For production

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
chmod +x git_pull.sh  # This doesn't seem to work!
chmod +x /home/fov/Desktop/JetsonConfig/git_pull_service/git_pull.sh
chmod +x git_pull_setup.sh
./git_pull_setup.sh


# ----------- Setup the web app listener (i.e. jetson_simulator.py) service -----------
cd ~/Desktop/FOVCamerasWebApp/jetson/configuring_jetsons
chmod +x web_app_listener_setup.sh 
./web_app_listener_setup.sh

