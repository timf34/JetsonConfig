#!/bin/bash

# Define the service file content

echo "[Unit]
Description=AWS IoT Device Shadow Python Script Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/fov/Desktop/JetsonConfig/device_shadow_config/aws_iot_device_shadow_script.py
Restart=on-failure
User=fov

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/aws_iot_device_shadow.service

# Reload the systemd daemon
systemctl daemon-reload

# Enable the service so it starts on boot
systemctl enable aws_iot_device_shadow.service

# Start the service
systemctl start aws_iot_device_shadow.service

# Print the status
systemctl status aws_iot_device_shadow.service

echo "Service has been set up and started!"
