import boto3
import fastparquet
from kafka import KafkaConsumer 
from datetime import datetime
import os 
from dotenv import load_dotenv 
import json
import pandas as pd

load_dotenv()

consumer = KafkaConsumer(
    'banking_server.public.customers',
    'banking_server.public.accounts',
    'banking_server.public.transactions',
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    auto_offset_commit = 'earliest',
    enable_auto_commit = True,
    value_deserializer = lambda x: json.loads(x.decode('utf-8'))
)
s3 = boto3.client(
    's3',
    endpoint_url=os.getenv("MINIO_ENDPOINT"),
    aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("MINIO_SECRET_KEY")
)
bucket = os.getenv("MINIO_BUCKET")
#bucket = os.getenev("MINIO_BUCKET")
if bucket not in [b['Name'] for b in s3.list_buckets()['Buckets']]:
    s3.create_bucket(Bucket=bucket)
def write_to_minio(topic, records):
    if not records:
        return 
    df = pd.DataFrame(records)
    date_str = datetime.now().strftime('%Y-%m-%d')
    file_path = f'{topic}/{date_str}.parquet'
    df.to_parquet(file_path, engine='fastparquet', index=False)
    s3_key = f'{topic}/date={date_str}/{datetime.now().strftime("%H%M%S%f")}.parquet'
    s3.upload_file(file_path, bucket, s3_key)
    os.remove(file_path)

batch_size = 50 

buffer_dict = {
    "banking_server.public.customers":  [],
    "banking_server.public.accounts": [],
    "banking_server.public.transactions": []
}

for message in consumer:
    topic = message.topic # topic = message.topic evnt = message.value payload = event.get( record = payload.get("after")
    event = message.value
    payload = event.get("payload", {})
    record = payload.get("after")

    if record: 
        buffer_dict[topic].append(record)
        if len(buffer_dict[topic]) >= batch_size:
            write_to_minio(topic.split('.')[-1], buffer_dict[topic])
            buffer_dict[topic] = []
