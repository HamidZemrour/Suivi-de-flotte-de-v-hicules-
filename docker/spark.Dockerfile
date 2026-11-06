# syntax=docker/dockerfile:1
FROM apache/spark:3.5.3-python3
USER root
RUN --mount=type=secret,id=proxy_ca if [ -f /run/secrets/proxy_ca ]; then export PIP_CERT=/run/secrets/proxy_ca; fi; pip install --no-cache-dir boto3==1.35.90
WORKDIR /project
COPY jobs jobs
COPY app/domain.py /project/jobs/domain.py
USER 185
