# syntax=docker/dockerfile:1
FROM python:3.11-slim
WORKDIR /project
COPY requirements.txt .
RUN --mount=type=secret,id=proxy_ca if [ -f /run/secrets/proxy_ca ]; then export PIP_CERT=/run/secrets/proxy_ca; fi; pip install --no-cache-dir -r requirements.txt
COPY app app
ENV PYTHONPATH=/project/app
