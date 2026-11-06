@echo off
cd /d "%~dp0"
echo Etape 2 : arret de la collecte pour liberer la memoire.
docker compose --env-file .env.windows8g stop simulator bridge spark-stream
if errorlevel 1 exit /b 1
docker compose --env-file .env.windows8g up --build -d spark-batch dashboard
if errorlevel 1 exit /b 1
docker compose --env-file .env.windows8g exec -T spark-batch python3 -c "from urllib.request import Request,urlopen; print(urlopen(Request('http://localhost:8090/run',data=b'',method='POST'),timeout=1800).read().decode())"
if errorlevel 1 (
  echo Calcul echoue. Verifiez que Silver existe et consultez les journaux.
  pause
  exit /b 1
)
echo Tableau de bord : http://localhost:8501
pause
