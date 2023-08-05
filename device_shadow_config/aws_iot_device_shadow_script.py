import json
import os
import time
import shutil
import psutil
import subprocess
import socket
import speedtest
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
from datetime import datetime

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
TEN_MINUTE_TIMEOUT_IN_SECONDS = 600
HOURLY_TIMEOUT_IN_SECONDS = 3600
DAILY_TIMEOUT_IN_SECONDS = 86400


class DeviceMetrics:

    def __init__(self):
        pass

    @staticmethod
    def get_storage_info():
        total, used, free = shutil.disk_usage("/")
        return {
            "total (GB)": total / 1e9,   # Convert to GB
            "used (GB)": used / 1e9,     # Convert to GB
            "free (GB)": free / 1e9      # Convert to GB
        }

    @staticmethod
    def get_memory_info():
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        return {
            "total (GB)": int(lines[0].split()[1]) / 1e6,      # Convert to GB
            "free (GB)": int(lines[1].split()[1]) / 1e6,       # Convert to GB
            "available (GB)": int(lines[2].split()[1]) / 1e6   # Convert to GB
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
        active_services = subprocess.check_output(['systemctl', 'list-units', '--type=service', '--state=running']).decode('utf-8')
        failed_services = subprocess.check_output(['systemctl', 'list-units', '--type=service', '--state=failed']).decode('utf-8')

        def parse_services(raw_output):
            lines = [line.strip() for line in raw_output.split('\n') if line]
            # Remove the header (1st line) as we'll hardcode the headers for parsing
            lines = lines[1:]
            
            services = []
            for line in lines:
                parts = line.split(maxsplit=4)
                # The split might produce more than 5 parts if DESCRIPTION had spaces. In that case, the last part will contain the remaining parts
                if len(parts) > 5:
                    parts = parts[:4] + [" ".join(parts[4:])]
                
                if len(parts) == 5:  # Ensure the line was in expected format
                    service_data = {
                        "UNIT": parts[0],
                        "LOAD": parts[1],
                        "ACTIVE": parts[2],
                        "SUB": parts[3],
                        "DESCRIPTION": parts[4]
                    }
                    services.append(service_data)
            
            return services


        return {
            "active": parse_services(active_services),
            "failed": parse_services(failed_services)
        }

    @staticmethod
    def get_network_info():
        # Note: This only measures current usage
        net_io_start = psutil.net_io_counters()
        time.sleep(1)  # Wait for 1 second
        net_io_end = psutil.net_io_counters()

        # Calculate the difference in bytes over the interval
        bytes_sent_per_sec = net_io_end.bytes_sent - net_io_start.bytes_sent
        bytes_recv_per_sec = net_io_end.bytes_recv - net_io_start.bytes_recv

        # Convert bytes per second to megabits per second (1 byte = 8 bits, 1 megabit = 10^6 bits)
        mbps_sent = (bytes_sent_per_sec * 8) / 1e6
        mbps_received = (bytes_recv_per_sec * 8) / 1e6

        return {
            "upload_speed_mbps": mbps_sent,
            "download_speed_mbps": mbps_received
        }

    # @staticmethod
    # def get_bandwidth():
    #     # Note: this method takes a while to execute
    #     st = speedtest.Speedtest()
        
    #     # Get best server based on ping
    #     st.get_best_server()
        
    #     # Measure download and upload speed
    #     download_speed = st.download() / 1e6  # Convert from bits per second to Mbps
    #     upload_speed = st.upload() / 1e6      # Convert from bits per second to Mbps

    #     return {
    #         "download_speed_mbps": download_speed,
    #         "upload_speed_mbps": upload_speed
    #     }

    @staticmethod
    def get_network_latency(host="8.8.8.8"):
        try:
            output = subprocess.check_output(["ping", "-c", "4", host])
            # Take the average from the 'min/avg/max/mdev' line
            avg_latency = output.splitlines()[-1].split(b'/')[4]
            return float(avg_latency)
        except:
            return None

    @staticmethod
    def get_local_ip():
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)

    @staticmethod
    def get_datetime():
        now = datetime.now()
        formatted_datetime = now.strftime("%H:%M - %d/%m/%Y")
        return formatted_datetime

    def collect_metrics(self):
        return {
            "datetime": self.get_datetime(),
            "storage": self.get_storage_info(),
            "memory": self.get_memory_info(),
            "cpu": self.get_cpu_usage(),
            "temperature": self.get_temperature(),
            "services": self.get_running_services(),
            "network (Mbps)": self.get_network_info(),
            # "bandwidth (Mbps)": self.get_bandwidth(),
            "network_latency (ms)": self.get_network_latency(),
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


def main():
    metrics_collector = DeviceMetrics()
    shadow_updater = DeviceShadowUpdater(THING_NAME, HOST, ROOT_CA, PRIVATE_KEY, CERTIFICATE)

    try:
        shadow_updater.connect()
    except Exception as e:
        print(f"Error connecting to AWS IoT: {e}")
        return

    while True:
        try:
            metrics = metrics_collector.collect_metrics()
            shadow_updater.update_shadow(metrics)
            time.sleep(TEN_MINUTE_TIMEOUT_IN_SECONDS)
        except Exception as e:
            print(f"Error while collecting/updating metrics: {e}")


def dev() -> None:
    # Temp function for testing the outputs
    metrics_collector = DeviceMetrics()
    try:
        metrics = metrics_collector.collect_metrics()
        print(json.dumps(metrics, indent=2))
    except Exception as e:
        print(f"Error while collecting metrics: {e}")



if __name__ == "__main__":
    main()
    # dev()
