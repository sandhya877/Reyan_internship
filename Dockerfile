FROM apache/airflow:2.7.2

COPY --chown=airflow:root test_dag.py /opt/airflow/dags
