from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app import fetch_weather, save_to_csv
from preprocess import preprocess_data
from train_model import train_model  # Import train_model function

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}

def collect_weather_data():
    logging.info("Starting weather data collection")
    weather = fetch_weather()
    save_to_csv(weather)
    logging.info("Weather data collected and saved successfully")

with DAG(
    'weather_pipeline',
    default_args=default_args,
    description='Weather data collection, preprocessing, and model training pipeline',
    schedule=timedelta(seconds=30),  # Running every 30 seconds
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

    train = PythonOperator(
        task_id='train_model',
        python_callable=train_model,  # Call the train_model function
        op_kwargs={'input_file': 'data/processed_data.csv', 'output_file': 'data/model.pkl', 'test_size': 0.2},  # Provide arguments for train_model
    )

    # Set task dependencies
    collect_data >> preprocess >> train  # Train runs after preprocess
