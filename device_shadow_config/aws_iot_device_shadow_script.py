import json
import os
import time
import shutil
import psutil
import subprocess
import socket
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient



# Configuration
try:
    THING_NAME = os.environ['DEVICE_NAME']
except KeyError:
    print("Please set the environment variable DEVICE_NAME (i.e. marvel-fov-n)")
    exit(1)

HOST = "a3lkzcadhi1yzr-ats.iot.eu-west-1.amazonaws.com"
ROOT_CA = "/home/fov/aws-iot-certs/AmazonRootCA1.pem"
PRIVATE_KEY = "/home/fov/aws-iot-certs/private.pem.key"
CERTIFICATE = "/home/fov/aws-iot-certs/certificate.pem.crt"
TIMEOUT_SECONDS: int = 600  # update every 10 minutes


class DeviceMetrics:

    def __init__(self):
        pass

    @staticmethod
    def get_storage_info():
        total, used, free = shutil.disk_usage("/")
        return {
            "total": total,
            "used": used,
            "free": free
        }

    @staticmethod
    def get_memory_info():
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        return {
            "total": int(lines[0].split()[1]),
            "free": int(lines[1].split()[1]),
            "available": int(lines[2].split()[1])
        }

    @staticmethod
    def get_cpu_usage():
        return psutil.cpu_percent(interval=1)

    @staticmethod
    def get_temperature():
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            return int(f.read()) / 1000.0

    @staticmethod
    def get_running_services():
        services = subprocess.check_output(['systemctl', 'list-units', '--type=service', '--state=running']).decode('utf-8')
        failed_services = subprocess.check_output(['systemctl', 'list-units', '--type=service', '--state=failed']).decode('utf-8')
        return {
            "active": services,
            "failed": failed_services
        }

    @staticmethod
    def get_network_info():
        net_io = psutil.net_io_counters()
        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_received": net_io.bytes_received
        }

    @staticmethod
    def get_local_ip():
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)

    def collect_metrics(self):
        return {
            "storage": self.get_storage_info(),
            "memory": self.get_memory_info(),
            "cpu": self.get_cpu_usage(),
            "temperature": self.get_temperature(),
            "services": self.get_running_services(),
            "network": self.get_network_info(),
            "local_ip": self.get_local_ip()
        }


class DeviceShadowUpdater:

    def __init__(self, thing_name, host, root_ca, private_key, certificate):
        self.thing_name = thing_name
        self.shadow_client_id = f"{thing_name}-shadow-client"

        self.shadow_client = AWSIoTMQTTShadowClient(self.shadow_client_id)
        self.shadow_client.configureEndpoint(host, 8883)
        self.shadow_client.configureCredentials(root_ca, private_key, certificate)
        self.shadow_client.configureConnectDisconnectTimeout(10)
        self.shadow_client.configureMQTTOperationTimeout(5)

    def connect(self):
        self.shadow_client.connect()

    def update_shadow(self, state):
        device_shadow = self.shadow_client.createShadowHandlerWithName(self.thing_name, True)
        state_json = json.dumps({"state": {"reported": state}})
        device_shadow.shadowUpdate(state_json, None, 5)


if __name__ == "__main__":
    metrics_collector = DeviceMetrics()
    shadow_updater = DeviceShadowUpdater(THING_NAME, HOST, ROOT_CA, PRIVATE_KEY, CERTIFICATE)
    shadow_updater.connect()

    while True:
        metrics = metrics_collector.collect_metrics()
        shadow_updater.update_shadow(metrics)
        time.sleep(TIMEOUT_SECONDS)
