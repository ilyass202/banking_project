import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()
connector_config = {
    "name": "postgres-connector",
    "config": {
        "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
        "task.max": "1",
        "database.hostname": os.getenv("POSTGRES_HOST"),
        "database.port": os.getenv("POSTGRES_PORT"),
        "database.user": os.getenv("POSTGRES_USER"),
        "database.password": os.getenv("POSTGRES_PASSWORD"),
        "database.dbname": os.getenv("POSTGRES_DB"),
        "topic.prefix": "banking_server",
        "plugin.name": "pgoutput",  
        "publication.autocreate.mode": "filtered",
        "slot.name": "slot_name",
        "table.include.list": "public.customers,public.accounts,public.transactions",
        "decimal.handling.mode": "double",
    }

}
url = "http://localhost:8083/connectors"
headers = {"Content-Type": "application/json"}
response = requests.post(url, headers=headers, data=json.dumps(connector_config))
if response.status_code == 201:
    print("Connector created successfully.")
else:
    print(f"Failed to create connector. Status code: {response.status_code}, Response: {response.text}")