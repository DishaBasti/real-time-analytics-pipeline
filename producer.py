import time
import json
import pandas as pd
from kafka import KafkaProducer
from datetime import datetime

# Kafka settings
KAFKA_BROKER = "localhost:9092"
TOPIC_MAP = {
    "North India": "viewership_north",
    "South India": "viewership_south",
    "East India": "viewership_east",
    "West India": "viewership_west"
}

DATA_FILE = "sample_data.csv"
SPEED_FACTOR = 3600  # Scale factor: 1 hour real time = 1 second in simulation

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

def start_producer():
    producer = KafkaProducer(bootstrap_servers=[KAFKA_BROKER], value_serializer=json_serializer)
    df = pd.read_csv(DATA_FILE)
    
    # Convert timestamp column to datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    for i in range(len(df)):
        message = df.iloc[i].to_dict()
        region = message.get("Region", "").strip()
        topic = TOPIC_MAP.get(region)

        if topic:
            producer.send(topic, message)
            print(f"Sent to {topic}: {message}")

        if i < len(df) - 1:
            current_time = df.iloc[i]['Timestamp']
            next_time = df.iloc[i + 1]['Timestamp']
            delay = (next_time - current_time).total_seconds()
            scaled_delay = delay / SPEED_FACTOR
            time.sleep(scaled_delay if scaled_delay > 0 else 0.01)

if __name__ == "__main__":
    start_producer()
