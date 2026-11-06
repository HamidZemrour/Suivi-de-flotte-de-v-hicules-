# Installer sur votre PC

## Windows

1. Installer Docker Desktop avec WSL2, puis démarrer Docker Desktop.
2. Télécharger le dépôt : bouton vert **Code → Download ZIP**, puis extraire tout.
3. Vérifier que le dossier extrait contient `docker-compose.yml`.
4. Double-cliquer `DEMARRER_WINDOWS.bat` ou ouvrir PowerShell dans ce dossier :

```powershell
docker compose up --build -d
```

5. Attendre les téléchargements et le premier calcul Airflow.
6. Ouvrir http://localhost:8501 pour la carte et http://localhost:8080 pour Airflow
   (compte de démonstration admin / admin).

## Linux / macOS

Installer Docker et Compose v2, extraire le ZIP, ouvrir le terminal dans le projet :

```bash
sh demarrer.sh
```

## Diagnostic

```bash
docker compose ps
docker compose logs --tail=100 spark-stream spark-batch airflow
```

Le premier DAG peut échouer si Silver n'est pas encore créée : vérifier le flux
puis relancer `refresh_gold` depuis Airflow. Vérifier que les deux DAG sont actifs.
Les paquets Spark/Hudi sont téléchargés sur Maven au premier lancement de chaque
conteneur Spark. Internet doit fonctionner ; ne pas désactiver TLS pour le contourner.
Prévoir 25 Go libres et 8 Go de RAM pour Docker. La chaîne complète reste à valider
sur votre PC ; les tests de code ne remplacent pas cette recette.

## Mise à jour et sauvegarde

Avec Git : `git pull`, puis `docker compose up --build -d`.
Arrêt conservant les données : `docker compose down`.
Ne pas utiliser `down -v` si vous souhaitez garder les données de démonstration.
