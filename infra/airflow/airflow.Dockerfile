FROM apache/airflow:3.0.0

USER airflow

# COPY the requirements file into the image
WORKDIR /opt/airflow
COPY ./requirements.txt .
COPY ./src/ ./src/
COPY ./setup.py .

# Install Python dependencies
# Add constraint (Docker-compatible way)
RUN pip install --no-cache-dir -r requirements.txt \
    --constraint https://raw.githubusercontent.com/apache/airflow/constraints-3.0.0/constraints-3.12.txt

# set the PYTHONPATH to include the src directory
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow/src"