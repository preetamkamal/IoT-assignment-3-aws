# Environmental Monitoring with AWS IoT Core

This project demonstrates how to connect an IoT environmental monitoring station to AWS IoT Core using the AWS IoT Device SDK for Python V2. The application simulates an environmental station that collects temperature, humidity, and CO2 data and publishes it to AWS IoT Core via MQTT.

## Features

- Connects securely to AWS IoT Core using X.509 certificates
- Simulates environmental sensor data (temperature, humidity, CO2)
- Publishes data to a specific MQTT topic at regular intervals
- Handles connection and graceful disconnection

## Requirements

- Python 3.6+
- AWS Account with IoT Core configured
- AWS IoT Device SDK for Python V2
- AWS IoT certificates and policies

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/environmental-monitoring.git
   cd environmental-monitoring
   ```

2. Install the AWS IoT Device SDK for Python V2:
   ```
   pip install awsiotsdk
   ```

## Setup

1. Place your AWS IoT certificates in the `new_certs` directory:
   - AmazonRootCA1.pem
   - private.pem.key
   - certificate.pem.crt

2. Update the configuration in [assigment-3-sol.py](assigment-3-sol.py) with your AWS IoT endpoint and region:
   ```python
   ENDPOINT = "your-endpoint.iot.region.amazonaws.com"
   AWS_REGION = "your-region"
   ```

3. (Optional) Adjust the CLIENT_ID, THING_NAME, and MQTT_TOPIC as needed.

## Usage

Run the application:
```
python assigment-3-sol.py
```

The application will connect to AWS IoT Core and start publishing simulated environmental data to the specified MQTT topic. Press `Ctrl+C` to stop the application.

## Data Format

The published data has the following JSON format:
```json
{
  "station_id": "EnvironmentalStation3",
  "temperature": 23.45,
  "humidity": 65.32,
  "co2": 450.21,
  "timestamp": 1627984562.345
}
```

## File Structure

- `assigment-3-sol.py` - Main application code
- `new_certs/` - Directory containing AWS IoT certificates
  - `AmazonRootCA1.pem` - AWS IoT Root CA certificate
  - `private.pem.key` - Device private key
  - `certificate.pem.crt` - Device certificate

## Troubleshooting

- Ensure your AWS IoT policy allows connecting and publishing to the specified topic
- Verify that the certificate paths in the code match your actual certificate locations
- Check AWS IoT Core logs for connection issues