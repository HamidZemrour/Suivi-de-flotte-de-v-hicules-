# syntax=docker/dockerfile:1
FROM apache/airflow:2.10.4-python3.11
RUN --mount=type=secret,id=proxy_ca if [ -f /run/secrets/proxy_ca ]; then export PIP_CERT=/run/secrets/proxy_ca; fi; pip install --no-cache-dir boto3==1.35.90
