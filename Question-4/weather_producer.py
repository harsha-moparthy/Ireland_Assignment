import time
import json
import random
from kafka import KafkaProducer
import pandas as pd
import os

# Path to the unzipped CSV file
csv_file_path = os.path.expanduser('weather.csv')

# Kafka producer configuration
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Load the Kaggle dataset (daily weather report)
weather_data = pd.read_csv(csv_file_path)

# Function to simulate weather data
def simulate_weather_update():
    random_row = weather_data.sample(n=1).iloc[0]
    weather_update = {
        'location': random_row['location_name'],
        'temperature': random_row['temperature_celsius'] + random.uniform(-2, 2), # adding random noise
        'humidity': random_row['humidity'] + random.uniform(-5, 5),       # adding random noise
        'precipitation': random_row['precip_mm'] + random.uniform(-0.1, 0.1) # adding random noise
    }
    return weather_update

# Produce messages to Kafka every second
try:
    for _ in range(60):  # Run for 60 seconds
        weather_update = simulate_weather_update()
        producer.send('global_weather', value=weather_update)
        print(f"Produced: {weather_update}")
        time.sleep(1)
finally:
    producer.close()
