import json
import pandas as pd
from kafka import KafkaConsumer

# Kafka consumer configuration
consumer = KafkaConsumer(
    'global_weather',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest', # Ensures reading from the beginning if new consumer
    enable_auto_commit=True,
    group_id='weather_consumer_group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Output CSV file
output_file = 'weather_updates.csv'

# Initialize an empty DataFrame to store the data
weather_df = pd.DataFrame(columns=['location', 'temperature', 'humidity', 'precipitation'])

# Consume messages from the Kafka topic
try:
    print("Starting to consume messages from 'global_weather' topic...")
    for message in consumer:
        weather_update = message.value
        print(f"Consumed: {weather_update}")
        # Append the new weather update to the DataFrame
        weather_df = weather_df._append(weather_update, ignore_index=True)
        # Save the DataFrame to a CSV file
        weather_df.to_csv(output_file, index=False)
except KeyboardInterrupt:
    print("Consumer stopped.")
finally:
    consumer.close()
    print("Consumer connection closed.")
