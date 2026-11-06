#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
docker compose up --build -d
printf '%s\n' 'Streamlit : http://localhost:8501' 'Airflow : http://localhost:8080 (admin / admin)'
