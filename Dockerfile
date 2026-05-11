FROM apache/airflow:2.7.1
WORKDIR /opt/airflow

USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
        procps \
        default-jre \
    && rm -rf /var/lib/apt/lists/*

USER airflow

COPY ./dags/* ./dags/
COPY ./spark/* ./spark/

RUN pip3 install apache-airflow-providers-apache-spark==4.1.1 pyspark==3.5.0 apache-airflow[statsd] airflow-exporter