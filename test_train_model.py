import os
import pandas as pd
import pytest
from sklearn.linear_model import LinearRegression
import pickle
from train_model import train_model  # Replace `your_module` with the actual .py file name (without .py)

@pytest.fixture
def sample_data(tmp_path):
    # Create sample DataFrame
    data = {
        'Humidity': [30, 45, 60, 75, 90],
        'Wind Speed': [5, 10, 15, 20, 25],
        'Temperature': [22, 24, 26, 28, 30]
    }
    df = pd.DataFrame(data)

    # Define input and output file paths
    input_csv = tmp_path / "test_data.csv"
    output_model = tmp_path / "test_model.pkl"

    # Save to CSV -
    df.to_csv(input_csv, index=False)

    return input_csv, output_model

def test_train_model_creates_model_file(sample_data):
    input_csv, output_model = sample_data

    # Run the training function
    train_model(str(input_csv), str(output_model))

    # Check if model file was created
    assert os.path.exists(output_model), "Model file was not created."

    # Optionally: check the model type
    with open(output_model, 'rb') as f:
        model = pickle.load(f)
    assert isinstance(model, LinearRegression), "Model is not a LinearRegression instance."
