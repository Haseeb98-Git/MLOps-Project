import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import mlflow
import mlflow.sklearn
import argparse

#mlflow.set_tracking_uri("http://127.0.0.1:5000") # for the local system
mlflow.set_tracking_uri("http://mlflow:5000") # for the container
def train_model(input_file='data/processed_data.csv', output_file='data/model.pkl', test_size=0.2):
    # Read processed data
    df = pd.read_csv(input_file)
    
    # Prepare features and target
    X = df[['Humidity', 'Wind Speed']]  # Features
    y = df['Temperature']  # Target
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    with mlflow.start_run():
        # Log parameters
        mlflow.log_param("model_type", "LinearRegression")
        mlflow.log_param("test_size", test_size)
        mlflow.log_param("random_state", 42)

        # Train the model
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # Evaluate the model
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)

        # Log metrics
        mlflow.log_metric("train_r2", train_score)
        mlflow.log_metric("test_r2", test_score)

        print(f"Training R² score: {train_score:.3f}")
        print(f"Testing R² score: {test_score:.3f}")

        # Save the model using both pickle and MLflow
        with open(output_file, 'wb') as f:
            pickle.dump(model, f)
        print(f"Model saved to {output_file}")
        
        # Save the model using MLflow
        mlflow.sklearn.log_model(model, "model")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='data/processed_data.csv')
    parser.add_argument('--output', default='data/model.pkl')
    parser.add_argument('--test_size', type=float, default=0.2)
    args = parser.parse_args()

    train_model(input_file=args.input, output_file=args.output, test_size=args.test_size)
