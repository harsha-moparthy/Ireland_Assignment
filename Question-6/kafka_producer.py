import time
import json
import random
from kafka import KafkaProducer
import pandas as pd
import os
import argparse

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
def simulate_weather_update(args):
    country = args.country if args.country else None
    global weather_data
    if country: 
        weather_data = weather_data[weather_data["country"] == country]
    else:
        weather_data = weather_data
    random_row = weather_data.sample(n=1).iloc[0]
    random_row.last_updated = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    return random_row.to_json()

# Produce messages to Kafka every second
def produce(args):
    try:
        for _ in range(60):  # Run for 60 seconds
            weather_update = simulate_weather_update(args)
            producer.send('global_weather', value=weather_update)
            print(f"Produced: {weather_update}")
            time.sleep(1)
    finally:
        producer.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--country", help="Country name to filter the weather data")
    args = parser.parse_args()
    produce(args)
    
    