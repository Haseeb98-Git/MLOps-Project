from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import fetch_weather, save_to_csv
from preprocess import preprocess_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def collect_weather_data():
    weather = fetch_weather()
    save_to_csv(weather)

with DAG(
    'weather_pipeline',
    default_args=default_args,
    description='Weather data collection and preprocessing pipeline',
    schedule_interval=timedelta(hours=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['weather', 'dvc'],
) as dag:

    collect_data = PythonOperator(
        task_id='collect_weather_data',
        python_callable=collect_weather_data,
    )

    preprocess = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data,
    )

    # Set task dependencies
    collect_data >> preprocess 