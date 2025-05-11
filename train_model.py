import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def train_model(input_file='processed_data.csv', output_file='model.pkl'):
    # Read processed data
    df = pd.read_csv(input_file)
    
    # Prepare features and target
    X = df[['Humidity', 'Wind Speed']]  # Features
    y = df['Temperature']  # Target
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Print model performance
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print(f"Training R² score: {train_score:.3f}")
    print(f"Testing R² score: {test_score:.3f}")
    
    # Save the model
    with open(output_file, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved to {output_file}")

if __name__ == "__main__":
    train_model() 