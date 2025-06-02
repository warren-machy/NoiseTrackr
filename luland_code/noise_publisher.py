import time
from datetime import datetime
import sounddevice as sd
import numpy as np
from scipy.fft import fft
import paho.mqtt.client as mqtt

# MQTT Broker
broker_address = "localhost"
topic = "noise"

# Initialize MQTT Client
client = mqtt.Client("NoiseSensor")

# Connect to MQTT Broker
client.connect(broker_address)

def measure_sound():
    duration = 10  # Duration to measure sound in seconds
    fs = 44100  # Sampling frequency
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    fft_result = fft(recording.flatten())
    freqs = np.fft.fftfreq(len(recording), 1 / fs)
    # Calculate sound level in dB from FFT result
    magnitude_spectrum = np.abs(fft_result)
    db = 20 * np.log10(np.max(magnitude_spectrum))
    return db

print('Date,Time,Sound Level (dB)')

while True:
    # Get current date and time
    now = datetime.now()
    date_time = now.strftime('%Y-%m-%d,%H:%M:%S')
    
    # Measure sound level in dB
    sound_level_db = measure_sound()
    
    # Output date, time, and sound level
    print('{},{:,.2f}'.format(date_time, sound_level_db))
    
    # Publish noise level to MQTT Broker
    client.publish(topic, payload="{},{:,.2f}".format(date_time, sound_level_db))
    
    time.sleep(10)