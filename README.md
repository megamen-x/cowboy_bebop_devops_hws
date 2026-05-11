# cowboy_bebop_devops_hws
Домашние задания по курсу "DevOps практики и инструменты", весна 2026

# ЛР 3. Github + CI

## Содержимое
* `Dockerfile` - образ на основе `apache/airflow:2.7.1` с установленными `procps`, `default-jre` и провайдером `apache-airflow-providers-apache-spark`; копирует DAG’и и Spark‑скрипты.
* `docker-compose.yml` - оркестрация сервисов: `postgres`, `spark-master`, `spark-worker`, `airflow-init`, `airflow-scheduler`, `airflow-webserver`.
* `dags/spark_dag.py` - DAG `spark_example_dag`, запускающий Spark‑приложение через `SparkSubmitOperator`.
* `spark/test_script.py` - Spark‑задание, которое создает `SparkSession`, строит тестовый DataFrame и выводит его содержимое.
* `.github/workflows/.github-ci.yaml` - CI-пайплайн, состоящий из четырех стадий: test (проверка на наличие директорий `dags` и `spark` в репозитории), build (автоматически не выполняется для веток с названием `feature/...`), deploy (автоматически для веток `main`, `master` и `develop`) и cleanup.

