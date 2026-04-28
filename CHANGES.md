## [2.0.0]
  - Dockerfile: добавлен шаг установки пакетов `procps` и `default-jre` для поддержки Spark-submit
  - Dockerfile: настроена смена пользователя `root/airflow` для корректной работы сервисов и прав доступа
  - docker-compose.yml: добавлены сервисы `spark-master` и `spark-worker
  - docker-compose.yml: добавлен volume `./spark:/opt/airflow/spark` для монтирования Spark‑скриптов
  - Добавлен новый DAG `spark_example_dag`, использующий `SparkSubmitOperator` для запуска PySpark‑задания
  - Добавлен Spark‑скрипт `spark/test_script.py`, создающий тестовый DataFrame через `SparkSession` и выводящий его содержимое

## [1.0.0]
  - Dockerfile на основе Airflow 2.7.1
  - docker-compose.yml с LocalExecutor, удалены лишние сервисы
  - Добавлен простейший DAG (считает сумму квадратов)
