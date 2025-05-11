import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess_data(input_file='/data/raw_data.csv', output_file='/data/processed_data.csv'):
    # Read the raw data
    df = pd.read_csv(input_file)
    
    # Handle missing values
    df = df.fillna(method='ffill')  # Forward fill for missing values
    
    # Normalize numerical columns
    numerical_cols = ['Temperature', 'Humidity', 'Wind Speed']
    scaler = StandardScaler()
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    
    # Save processed data
    df.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")


if __name__ == "__main__":
    preprocess_data()
