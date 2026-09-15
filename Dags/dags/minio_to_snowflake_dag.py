import os 
from datetime import datetime, timedelta 

from dotenv import load_dotenv
from airflow import DAG
from airflow.operators.python import PythonOperator 
import boto3
import snowflake.connector 

load_dotenv()

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
BUCKET = os.getenv("MINION_BUCKET")
LOCAL_DIR = os.getenv("MINIO_LOCAL_DIR", '/tmp/minio_downloads')

# --- Snowflake Config 

SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DB = os.getenv("SNOWFLAKE_DB")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")

TABLES = ["customers", "accounts", "transactions"]

# --- Python Callables --

def download_from_minio():
    os.makedirs(LOCAL_DIR, exist_ok= True)
    s3 = boto3.client(
        "s3", 
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY
    )
    local_files = {}
    for table in TABLES:
        prefix = f'{table}/'
        resp = s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix)
        objects = resp.get("Contents", [])
        local_files[table] = []
        for obj in objects:
            key = obj["Key"]
            local_path = os.path.join(LOCAL_DIR, os.path.basename(key))
            s3.download_file(BUCKET, key, local_path)
            local_files[table].append(local_path)
    return local_files
def load_to_snowflake(**kwargs):
    local_files = kwargs['ti'].xcom_pull(task_ids='download_from_minio')
    if not local_files:
        return
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DB,
        schema=SNOWFLAKE_SCHEMA
    )
    curr = conn.cursor()
    for tab, files in local_files.items():
        if not files:
            return
        for file in files:
            curr.execute(f"PUT file://{file} @%{tab}")
            print(f"upload the file {file} into the table {tab}")
            
            copy_sql = f""" copy into {tab} from @%{tab} file_format = (TYPE= PARQUET) ON_ERROR='CONTINUE'"""
            curr.execute(copy_sql)
            print(f"copy the file {file} into the table {tab}")
    curr.close()
    conn.close()



default_args = {
        "owner": "airflow",
        "retries": 1,
        "retry_delay": timedelta(minutes=1)    }

with DAG(
    dag_id = "minio_to_snowflake_dag",
    default_args=default_args,
    description = "this dag loads data from Minio to Snowflake",
    schedule_interval= '*/1 * * * *',
    start_date = datetime(2025, 1, 1),
    catchup = False
) as dag:
    task1 = PythonOperator(
        task_id = "download_from_minio",
        python_callable=download_from_minio
    )
    task2 = PythonOperator(
        task_id = "load_to_snowflake",
        python_callable=load_to_snowflake,
        provide_context=True
    )

    task1 >> task2