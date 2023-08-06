The following commands need to be ran and set up interactively 


### IMX477 Driver (ran before `initial_jetson_setup.sh`)

`sudo /opt/nvidia/jetson-io/jetson-io.py`

Select the following options:
- Configure CSI Connector (?)
- IMX477 Dual 
- Configure and reboot


### Transferring AWS IOT Certificates (ran before `initial_jetson_setup.sh`)

Run this command from my laptop from the directory containing the certificates (it transfers all files in the directory):

`scp * fov@192.168.234.2:/home/fov/aws-iot-certs/`


### AWS IOT Device Client (ran after `initial_jetson_setup.sh`)

```bash
cd ~/Desktop/aws-iot-device-client
sudo ./setup.sh
```

Test