# cowboy_bebop_devops_hws
Домашние задания по курсу "DevOps практики и инструменты", весна 2026

# ЛР 4. Loki + Prometheus + Grafana

## Содержимое
* `Dockerfile` - образ на основе `apache/airflow:2.7.1` с установленными `procps`, `default-jre` и провайдером `apache-airflow-providers-apache-spark`; копирует DAG’и и Spark‑скрипты.
* `docker-compose.yml` - оркестрация сервисов: `postgres`, `spark-master`, `spark-worker`, `airflow-init`, `airflow-scheduler`, `airflow-webserver`, `loki`, `allow`, `prometheus`, `grafana`.
* `dags/spark_dag.py` - DAG `spark_example_dag`, запускающий Spark‑приложение через `SparkSubmitOperator`.
* `spark/test_script.py` - Spark‑задание, которое создает `SparkSession`, строит тестовый DataFrame и выводит его содержимое.

## Локальный деплой

### Предварительные требования
* Установлены Docker и Docker Compose (или Docker Desktop с `docker compose` plugin).

### Шаги
1. Склонировать репозиторий
2. Запустить контейнеры

```bash
docker compose up --build -d
```

3. Дождаться сборки без ошибок (health для всех), если контейнер с postgres не собирается, то:
```bash
sudo systemctl stop postgresql
```
И запустить compose up повторно

4. Открыть браузер по адресу `http://localhost:8080` и ввести логин и пароль, которые заданы в compose:
   * Логин: `admin`
   * Пароль: `admin123`
5. Создать подключение к Spark в Airflow: Admin → Connections → "+":
   * Connection Id: `spark_default`
   * Connection Type: `Spark`
   * Host: `spark://spark-master`
   * Port: `7077`
   * Extra: `{}` (без этого не подключалось)
6. На странице DAGs найти и запустить `spark_example_dag`, подождать завершения
7. Посмотреть на Spark Web UI `http://localhost:4040` состояние приложения в `Completed Applications`
8. Проверить состояние метрик по адресу `http://localhost:8080/admin/metrics`
9. Перейти на `http://localhost:9090` в Prometheus и во вкладке `Status → Targets` проверить подключение к airflow
10. Для тестов можно сделать запрос в Prometheus в разделе `Graph`
11. Далее зайти в Grafana `http://localhost:3000` и подключить Loki и Prometheus в `Connections → Data sources`
12. В Grafana на вкладке `Explore` настроить запросы в Airflow и добавить их на дэшборд

### Выполнение практической работы

Просмотр логирования в Alloy (через логи контейнера)

![alloy conf](assets/alloy_conf.png)

#### Метрики для DAG sum_of_squares_calculator

Проверка подключения к admin/metrics в Prometheus (Status → Targets):

![prometheus tracks](assets/prometheus_tracks.png)

Запрос состояния DAG из Airflow через Prometheus:

![prometheus metrics](assets/prometheus_metrics.png)

Подключение Loki в Grafana и вывод логов результатов работы DAG: 

![grafana query](assets/grafana_query.png)

Подключение Prometheus в Grafana и вывод логов статуса DAG в Airflow: 

![grafana prom](assets/grafana_prom.png)

#### Метрики для DAG spark_example_dag

Проверка подключения к admin/metrics в Prometheus:

![prometheus tracks](assets/prometheus_tracks_dag.png)

Подключение Loki в Grafana аналогично как для sum_of_squares_calculator

Подключение Prometheus в Grafana и вывод логов статуса DAG в Airflow:

![prometheus metrics](assets/prometheus_metrcis_dag.png)

Финальный дэшборд с логами состояния через Loki и Prometheus:

![outputs](assets/dag_grafana_outputs.png)


### Остановка
```bash
docker compose down -v  # удалит тома БД (чистый сброс)
```

## Примечания
* DAG работает только по ручному триггеру, расписание отсутствует (`schedule_interval=None`).
* Spark‑кластер (`spark-master` и `spark-worker`) стартует вместе с остальными сервисами и доступен по портам `4040` (веб‑интерфейс) и `7077` (подключения).
* Все скрипты, лежащие в локальной папке `spark/`, монтируются в контейнер Airflow по пути `/opt/airflow/spark`.
* Логи Airflow сохраняются в локальной директории `./logs`.
* Благодаря `apache-airflow[statsd]` и `airflow-exporter` удалось настроить admin/metrics для Airflow (без них страница 404 выдавала).
* Проверки и графики Loki и Prometheus были настроены и проверены для двух DAG-скриптов из Airflow.
* Финальный [docker-compose.yml](./docker-compose.yml)
