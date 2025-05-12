import os
import pytest
import requests
from datetime import datetime
from app import fetch_weather, save_to_csv
import csv

def test_fetch_weather():
    # Make an actual API request to fetch weather data
    weather_data = fetch_weather()

    # Validate the structure of the returned data
    assert 'Date and Time' in weather_data
    assert 'Temperature' in weather_data
    assert 'Humidity' in weather_data
    assert 'Wind Speed' in weather_data
    assert 'Weather Condition' in weather_data

    # Validate the values returned by the function
    assert isinstance(weather_data['Temperature'], (int, float)), "Temperature should be a number"
    assert isinstance(weather_data['Humidity'], int), "Humidity should be an integer"
    assert isinstance(weather_data['Wind Speed'], (int, float)), "Wind Speed should be a number"
    assert isinstance(weather_data['Weather Condition'], str), "Weather Condition should be a string"

    # Check if the 'Date and Time' is a valid datetime string
    try:
        datetime.strptime(weather_data['Date and Time'], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        pytest.fail("Date and Time format is incorrect.")

def test_save_to_csv():
    # Fetch the weather data from the actual API
    weather_data = fetch_weather()

    # Prepare file path
    csv_file = 'test_weather_data.csv'

    # Call the save_to_csv function
    save_to_csv(weather_data, filename=csv_file)

    # Check if the CSV file is created
    assert os.path.exists(csv_file), "CSV file was not created."

    # Read the CSV and validate content
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        # Validate that we saved exactly one entry
        assert len(rows) == 1, "CSV file should contain exactly one entry."

        # Validate that all necessary columns exist
        assert 'Date and Time' in rows[0], "Date and Time is missing in the CSV"
        assert 'Temperature' in rows[0], "Temperature is missing in the CSV"
        assert 'Humidity' in rows[0], "Humidity is missing in the CSV"
        assert 'Wind Speed' in rows[0], "Wind Speed is missing in the CSV"
        assert 'Weather Condition' in rows[0], "Weather Condition is missing in the CSV"

        # Validate the types/formats of the data
        assert isinstance(float(rows[0]['Temperature']), (int, float)), "Temperature should be a number"
        assert isinstance(int(rows[0]['Humidity']), int), "Humidity should be an integer"
        assert isinstance(float(rows[0]['Wind Speed']), (int, float)), "Wind Speed should be a number"
        assert isinstance(rows[0]['Weather Condition'], str), "Weather Condition should be a string"
        try:
            datetime.strptime(rows[0]['Date and Time'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            pytest.fail("Date and Time format in CSV is incorrect.")