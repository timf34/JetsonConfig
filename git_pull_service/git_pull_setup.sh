#!/bin/bash

# Provide user name as an argument while running this script
USER_NAME="fov"

# Change ownership and permissions of the FOVCamerasWebApp Git repository
sudo chown -R $USER_NAME:$USER_NAME /home/$USER_NAME/Desktop/FOVCamerasWebApp
sudo chmod -R 755 /home/$USER_NAME/Desktop/FOVCamerasWebApp

# Change ownership and permissions of the JetsonChowon Git repository
sudo chown -R $USER_NAME:$USER_NAME /home/$USER_NAME/Desktop/JetsonConfig
sudo chmod -R 755 /home/$USER_NAME/Desktop/JetsonConfig

# Make pull_git.sh executable
chmod +x /home/$USER_NAME/Desktop/JetsonConfig/git_pull_service/git_pull.sh

# Add the directory to the list of safe directories in Git's configuration
sudo git config --system --add safe.directory '*'

# Create a systemd service
echo "[Unit]
Description=Pull git on network connectivity
After=network.target

[Service]
User=$USER_NAME
Group=$USER_NAME
ExecStart=/home/$USER_NAME/Desktop/JetsonConfig/git_pull_service/git_pull.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/gitpull.service

# Reload systemd manager configuration
sudo systemctl daemon-reload

# Enable the service
sudo systemctl enable gitpull

# Start the service
sudo systemctl start gitpull
