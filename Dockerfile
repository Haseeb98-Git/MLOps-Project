FROM python:3.11

# Set working directory
WORKDIR /mlflow

# Install MLflow
RUN pip install mlflow

# Set the backend URI environment variable
ENV BACKEND_URI=sqlite:///mlflow.db

# Expose the MLflow UI port
EXPOSE 5000

# Run the MLflow UI
CMD ["mlflow", "ui", "--backend-store-uri", "sqlite:///mlflow.db", "--host", "0.0.0.0"]
