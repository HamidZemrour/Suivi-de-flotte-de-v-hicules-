# Windows avec 8 Go de RAM

La plateforme complete est lourde pour 8 Go. Ce mode tente une demonstration
**par etapes**, en evitant les deux JVM Spark simultanees. Il ne garantit pas
l'absence de saturation. Le mode continu complet du sujet est conserve dans
`docker-compose.yml` ; pour la soutenance complete, privilegier un PC du groupe
avec 16 Go ou plus, ou une machine distante adaptee.

## 1. Preparation

- Installer Docker Desktop pour Windows depuis le site officiel et choisir WSL2.
- Redemarrer Windows si demande, puis lancer Docker Desktop.
- Fermer les applications lourdes ; prevoir au moins 25 Go de disque libre.
- Verifier dans PowerShell : `wsl --status`, `docker version`, `docker compose version`.
- Si Docker ou WSL indique que la virtualisation est desactivee, suivre son diagnostic.

Pour limiter WSL2, creer ou modifier le fichier `%UserProfile%\.wslconfig`
avec le Bloc-notes. Conserver les autres reglages existants et ajouter/adapter :

```ini
[wsl2]
memory=4GB
processors=2
swap=4GB
```

Quitter Docker Desktop, lancer `wsl --shutdown` dans PowerShell (cela arrete
les sessions WSL ouvertes), puis relancer Docker Desktop. Le swap utilise le
disque : il peut eviter certains arrets mais ralentit fortement les calculs.
Si une limite memoire existe deja, verifier les reglages avant de la modifier.

## 2. Extraire le projet

Extraire entierement FleetPulse-ISSE05.zip dans un dossier court, par exemple
Documents\FleetPulse. Les fichiers caches comme `.env.windows8g` sont necessaires.
Le fichier `docker-compose.yml` doit se trouver dans le meme dossier que les .bat.

## 3. Etape 1 : collecter et nettoyer

Double-cliquer `WINDOWS_8GO_ETAPE1.bat`.
Attendre les telechargements et 2 a 5 minutes de collecte reussie.
Ouvrir http://localhost:9001 (fleetadmin / fleetpassword123).
Verifier dans le bucket fleet : bronze et silver_positions avec `.hoodie`.
Si Silver manque, ne pas passer a l'etape 2 ; verifier :

```powershell
docker compose --env-file .env.windows8g logs --tail=100 spark-stream
```

## 4. Etape 2 : calculer et afficher

Double-cliquer `WINDOWS_8GO_ETAPE2.bat`. Il arrete le generateur, le pont et
Spark Streaming, puis calcule Gold et KMeans avant d'ouvrir la restitution.
Ouvrir http://localhost:8501. Le flux est maintenant fige : les points ne
bougent plus. Il s'agit d'un resultat du pipeline, pas d'un suivi continu.
Le premier calcul peut prendre plusieurs minutes sur cette configuration.

## 5. Airflow, apres les premiers calculs

Pour montrer l'orchestration avec le streaming toujours arrete :

```powershell
docker compose --env-file .env.windows8g up --build -d postgres airflow
```

Airflow : http://localhost:8080 (admin / admin). Le DAG refresh_gold recalcule
les donnees deja presentes. Le rapport quotidien concerne son intervalle UTC
et peut etre vide si aucune donnee de cette date n'existe. Si Windows sature,
arreter cette etape et utiliser une machine plus puissante pour la demonstration
complete. Ne pas presenter ce mode sequentiel comme un streaming integral actif.

## 6. Arreter

```powershell
docker compose --env-file .env.windows8g down
```

Les donnees sont conservees. Si vous recommencez l'etape 1 et voulez limiter
la memoire, arretez Airflow et Postgres avant :

```powershell
docker compose --env-file .env.windows8g stop airflow postgres spark-batch dashboard
```

## Validation

La syntaxe Compose et les scripts de lancement ont ete controles. Les reglages
8 Go n'ont pas ete executes sur votre Windows. Les tests Spark et Hudi locaux
ont reussi ; l'integration complete Docker reste a verifier sur votre PC.
