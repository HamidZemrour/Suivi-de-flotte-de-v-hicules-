@echo off
cd /d "%~dp0"
docker compose up --build -d
if errorlevel 1 (
  echo Echec du lancement. Verifiez Docker Desktop et les journaux.
  pause
  exit /b 1
)
echo Ouvrez http://localhost:8501 apres le premier traitement Airflow.
echo Airflow : http://localhost:8080 - admin / admin
pause
