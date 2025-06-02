import paho.mqtt.client as mqtt
import os
from datetime import datetime

# MQTT Broker
broker_address = "xxx.xxx.xxx.xx"  # IP address of your MQTT broker
topic = "noise"

# Define the CSV file path
csv_file_path = "noise_data.csv"

# Initialize MQTT Client
client = mqtt.Client("NoiseSubscriber")

# Callback function for when the client successfully connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code " + str(rc))
    # Subscribe to the noise topic
    client.subscribe(topic)

# Callback function for when a message is received from the broker
def on_message(client, userdata, msg):
    try:
        print("Received message: " + msg.payload.decode())
        # Split the message by commas to extract date, time, and noise level
        parts = msg.payload.decode().split(",")
        if len(parts) >= 3:
            date_time = parts[0] + "," + parts[1]
            noise_level = float(parts[2])
            # Write noise data to the CSV file
            write_noise_data(date_time, noise_level)
        else:
            print("Invalid message format:", msg.payload.decode())
    except Exception as e:
        print("Error processing message:", e)

# Connect callback functions to client
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT Broker
client.connect(broker_address)

# Function to write noise data to CSV file
def write_noise_data(date_time, noise_level):
    try:
        with open(csv_file_path, 'a') as f:
            f.write(date_time + "," + str(noise_level) + "\n")
        print("Noise data written to CSV file.")
    except Exception as e:
        print("Error writing noise data to CSV file:", e)

# Start the MQTT client loop to listen for messages
client.loop_forever()
