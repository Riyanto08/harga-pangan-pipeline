from datetime import timedelta

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

with DAG(
    dag_id="harga_pangan_daily",
    description="Tarik harga PIHPS, muat ke BigQuery, lalu jalankan dbt build",
    schedule="0 14 * * 1-5",
    start_date=pendulum.datetime(2026, 10, 1, tz="Asia/Jakarta"),
    catchup=False,
    tags=["harga_pangan"],
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=10),
    },
) as dag:

    extract = BashOperator(
        task_id="extract_pihps",
        bash_command="cd /opt/project && python extract/extract_pihps.py",
    )

    load = BashOperator(
        task_id="load_bigquery",
        bash_command="cd /opt/project && python extract/load_bq.py",
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command="cd /opt/project/dbt_harga_pangan && /opt/airflow/dbt_venv/bin/dbt build",
    )

    extract >> load >> dbt_build