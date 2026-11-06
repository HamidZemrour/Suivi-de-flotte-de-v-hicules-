@echo off
cd /d "%~dp0"
echo Etape 1 : ingestion et stockage Silver. Docker Desktop doit etre demarre.
docker compose --env-file .env.windows8g up --build -d mqtt kafka minio simulator bridge spark-stream
if errorlevel 1 (
  echo Echec. Voir docs\WINDOWS_8GO.md
  pause
  exit /b 1
)
echo Attendez 2 a 5 minutes puis verifiez Silver dans MinIO : http://localhost:9001
echo Identifiants : fleetadmin / fleetpassword123
pause
