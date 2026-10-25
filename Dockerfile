FROM apache/airflow:3.2.0-python3.12

RUN pip install --no-cache-dir \
    "apache-airflow==${AIRFLOW_VERSION}" \
    requests \
    google-cloud-bigquery

RUN python -m venv /opt/airflow/dbt_venv \
    && /opt/airflow/dbt_venv/bin/pip install --no-cache-dir dbt-bigquery==1.12.1