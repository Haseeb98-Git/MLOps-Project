FROM python:3.11

# Set working directory
WORKDIR /app

# Copy the entire project directory, excluding venv folder (using .dockerignore)
COPY . /app

# Install dependencies from requirements.txt
RUN pip install -r /app/requirements.txt

# Remove the old airflow.cfg file if it exists (we'll recreate it)
RUN rm -f /app/airflow/airflow.cfg

# Set the AIRFLOW_HOME environment variable to the correct location
ENV AIRFLOW_HOME=/app/airflow

# Initialize Airflow database (migrate)
RUN airflow db migrate

# Install mlflow
RUN pip install mlflow

# Default command to run (overridden by Docker Compose)
CMD ["/bin/bash"]
