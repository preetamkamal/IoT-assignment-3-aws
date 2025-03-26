# import paho.mqtt.client as mqtt
# import ssl
# import json
# import random
# import time
# import datetime

# # AWS IoT endpoint (found in AWS IoT console under Settings)
# broker = "a2ao8aow8ghi9v-ats.iot.us-east-2.amazonaws.com"  # e.g., "abcdefghijklm.iot.us-east-1.amazonaws.com"
# port = 8883

# # Unique station ID
# station_id = "station_001"

# def generate_sensor_data():
#     return {
#         "station_id": station_id,
#         "temperature": round(random.uniform(-50, 50), 2),
#         "humidity": round(random.uniform(0, 100), 2),
#         "co2": random.randint(300, 2000),
#         "timestamp": datetime.datetime.utcnow().isoformat()
#     }

# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code " + str(rc))

# client = mqtt.Client()
# client.on_connect = on_connect

# # Set TLS parameters: adjust file paths to your downloaded certificates
# client.tls_set(ca_certs="./connect_device_package/station_001.cert.pem",
#                certfile="./root-CA.crt",
#                keyfile="./connect_device_package/station_001.private.key",
#                tls_version=ssl.PROTOCOL_TLSv1_2)

# client.connect(broker, port, keepalive=60)
# client.loop_start()

# while True:
#     sensor_data = generate_sensor_data()
#     topic = f"environment/{station_id}/sensor"
#     client.publish(topic, json.dumps(sensor_data))
#     print("Published:", sensor_data)
#     time.sleep(10)  # adjust publishing frequency as needed



import random
import time
import ssl
from awscrt import mqtt
from awsiot import mqtt_connection_builder
import uuid
import json

# AWS IoT Core Configuration - Replace with your actual values
ENDPOINT = "a2ao8aow8ghi9v-ats.iot.us-east-2.amazonaws.com"  # e.g., 'xxxxxxxxxx-ats.iot.us-east-1.amazonaws.com'
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
