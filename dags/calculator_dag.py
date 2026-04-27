from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def generate_numbers(**context):
    """Генерирует список чисел от 1 до N"""
    N = context['params'].get('N', 10)
    numbers = list(range(1, N+1))
    context['ti'].xcom_push(key='numbers', value=numbers)
    return f"Сгенерировано {len(numbers)} чисел"

def sum_of_squares(**context):
    """Вычисляет сумму квадратов чисел"""
    numbers = context['ti'].xcom_pull(key='numbers', task_ids='generate_numbers')
    result = sum(x**2 for x in numbers)
    context['ti'].xcom_push(key='result', value=result)
    return f"Сумма квадратов = {result}"

def print_result(**context):
    """Выводит результат"""
    result = context['ti'].xcom_pull(key='result', task_ids='sum_of_squares')
    print(f"Результат вычисления: {result}")
    return result

with DAG(
    dag_id='sum_of_squares_calculator',
    default_args=default_args,
    description='DAG для вычисления суммы квадратов чисел от 1 до N',
    schedule_interval=None,
    catchup=False,
    tags=['calculation', 'example'],
    params={'N': 10},
) as dag:

    t1 = PythonOperator(
        task_id='generate_numbers',
        python_callable=generate_numbers,
    )

    t2 = PythonOperator(
        task_id='sum_of_squares',
        python_callable=sum_of_squares,
    )

    t3 = PythonOperator(
        task_id='print_result',
        python_callable=print_result,
    )

    t1 >> t2 >> t3