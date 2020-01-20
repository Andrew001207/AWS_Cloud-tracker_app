from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
from coords import parseCoords

location = {}

# Custom MQTT message callback
def customCallback(client, userdata, message):
    global location
    print('UPDATE LOCATION')
    print("Received a new message: ")
    print(message.payload)
    result = parseCoords(str(message.payload))
    # if result is not None:
    location[0] = result
    print(location)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

host = 'a28aowjqltdgxj-ats.iot.us-west-2.amazonaws.com'
rootCAPath = 'cert/AmazonRootCA1.pem'
certificatePath = 'cert/89e9febeb8-certificate.pem.crt'
privateKeyPath = 'cert/89e9febeb8-private.pem.key'
port = 8883
clientId = 'Python_test_subscriber'
topic = 'SmartBeacon7600_GPS'

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.ERROR)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
time.sleep(2)

if __name__ == '__main__':
    while True:
        time.sleep(0.1)