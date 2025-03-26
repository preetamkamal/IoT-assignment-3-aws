import random
import time
import ssl
from awscrt import mqtt
from awsiot import mqtt_connection_builder
import uuid
import json

# AWS IoT Core Configuration 
ENDPOINT = "a2ao8aow8ghi9v-ats.iot.us-east-2.amazonaws.com" 
CLIENT_ID = "EnvironmentalStation3"  #Unique ID for each sensor
THING_NAME = "station_001" # Must match the 'thingName' in your policy
ROOT_CA = "./new_certs/AmazonRootCA1.pem" #Download from AWS
PRIVATE_KEY = "./new_certs/private.pem.key" #Download from AWS
CERTIFICATE = "./new_certs/certificate.pem.crt" #Download from AWS
AWS_REGION = "us-east-2"  # Replace with your AWS region


# Sensor ranges
TEMP_RANGE = (-50, 50)
HUMIDITY_RANGE = (0, 100)
CO2_RANGE = (300, 2000)

# MQTT Topic
MQTT_TOPIC = f"environmental/data/{CLIENT_ID}"  # Topic to publish to

# Create MQTT connection
mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    port=8883,
    cert_filepath=CERTIFICATE,
    pri_key_filepath=PRIVATE_KEY,
    ca_filepath=ROOT_CA,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=6
)

print("Connecting to {} with client ID '{}'...".format(ENDPOINT, CLIENT_ID))
connect_future = mqtt_connection.connect()

# Wait for connection to be established
connect_future.result()
print("Connected!")

def publish_message():
    temperature = round(random.uniform(*TEMP_RANGE), 2)
    humidity = round(random.uniform(*HUMIDITY_RANGE), 2)
    co2 = round(random.uniform(*CO2_RANGE), 2)

    message = {
        "station_id": CLIENT_ID,
        "temperature": temperature,
        "humidity": humidity,
        "co2": co2,
        "timestamp": time.time()
    }
    message_json = json.dumps(message)

    print(f"Publishing message to topic '{MQTT_TOPIC}': {message_json}")
    mqtt_connection.publish(
        topic=MQTT_TOPIC,
        payload=message_json,
        qos=mqtt.QoS.AT_LEAST_ONCE)
    time.sleep(5)

if __name__ == '__main__':
    try:
        while True:
            publish_message()
    except KeyboardInterrupt:
        print("Disconnecting...")
        disconnect_future = mqtt_connection.disconnect()
        disconnect_future.result()
        print("Disconnected!")
