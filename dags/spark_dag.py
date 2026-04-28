from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='spark_example_dag',
    default_args=default_args,
    description='Пример DAG для запуска Spark-задания',
    schedule_interval=None,
    catchup=False,
    tags=['spark'],
) as dag:

    spark_job = SparkSubmitOperator(
        task_id='run_spark_job',
        application='/opt/airflow/spark/test_script.py',
        name='airflow-spark-example',
        conn_id='spark_default',
        verbose=False,
    )

    spark_job