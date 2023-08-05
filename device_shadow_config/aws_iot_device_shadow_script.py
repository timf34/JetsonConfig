import json
import os
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

# Get the env variable DEVICE NAME using try except block which raises an exception if the variable is not set.
try:
    THING_NAME = os.environ['DEVICE_NAME']
    SHADOW_CLIENT = THING_NAME + "-shadow-client"
except KeyError:
    print("Please set the environment variable DEVICE_NAME (i.e. marvel-fov-n)")
    sys.exit(1)


# AWS IoT configuration.
HOST = "a3lkzcadhi1yzr-ats.iot.eu-west-1.amazonaws.com"
ROOT_CA = "/home/fov/aws-iot-certs/AmazonRootCA1.pem"
PRIVATE_KEY = "/home/fov/aws-iot-certs/private.pem.key"
CERTIFICATE = "/home/fov/aws-iot-certs/certificate.pem.crt"

# Initialize the AWS IoT MQTT Shadow Client.
shadow_client = AWSIoTMQTTShadowClient(SHADOW_CLIENT)
shadow_client.configureEndpoint(HOST, 8883)
shadow_client.configureCredentials(ROOT_CA, PRIVATE_KEY, CERTIFICATE)
shadow_client.configureConnectDisconnectTimeout(10)
shadow_client.configureMQTTOperationTimeout(5)

shadow_client.connect()

# Create a device shadow instance.
device_shadow = shadow_client.createShadowHandlerWithName(THING_NAME, True)

while True:
    # For demonstration purposes. In reality, you'd gather actual diagnostics here.
    reported_state = {
        "temperature": "35C",
        "memoryUsage": "2GB",
    }

    # Convert the Python dictionary to a JSON string.
    reported_state_json = json.dumps({"state": {"reported": reported_state}})
    
    # Update device shadow.
    device_shadow.shadowUpdate(reported_state_json, None, 5)

    # Wait before the next loop.
    time.sleep(60)  # e.g., update every minute
