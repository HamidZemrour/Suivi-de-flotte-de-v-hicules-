# Comprendre et présenter le projet

## Parcours d'une position

1. Un boîtier simulé crée un UUID, l'identifiant véhicule, l'heure UTC, la position et la vitesse.
2. MQTT livre le message au pont. Kafka le partitionne par véhicule et le conserve.
3. Spark archive le JSON en Bronze, isole les invalides, ajoute les règles et upsert Silver.
4. Airflow demande un calcul Gold. Spark ordonne les points et calcule les segments,
   agrège en SQL et entraîne KMeans sur les arrêts.
5. Streamlit lit les exports Gold ; Airflow produit le rapport quotidien.

## Trame orale proposée, à adapter au temps donné par l'enseignant

- Membre 1 : problème, données simulées, MQTT et Kafka.
- Membre 2 : zones Bronze/Silver/Gold, clés Hudi et doublons.
- Membre 3 : distance, SQL, géorepérage, KMeans et limites.
- Membre 4 : Airflow, carte et démonstration.
- Chaque membre présente aussi ses contributions réelles.

## Questions probables

**Pourquoi MQTT puis Kafka ?** MQTT est léger pour les objets connectés ; Kafka
conserve un journal partitionné et découple les producteurs des traitements.

**Pourquoi Hudi plutôt que des fichiers JSON ?** Hudi gère des clés et mises à jour
transactionnelles par table, versions de commits et lecture cohérente.

**Comment gérer les doublons ?** Même event_id conservé, dédoublonnage du micro-lot
et upsert Hudi. Ne pas prétendre à exactly-once sur toute la chaîne.

**Pourquoi KMeans ?** Trouver des zones d'arrêt sans étiquettes. Les positions sont
approximativement converties en kilomètres ; le nombre de clusters est fixé entre 2 et 3.
Il faut analyser les centres, tester plusieurs k et valider sur davantage de données.

**La distance est-elle exacte ?** Non : somme de segments GPS échantillonnés. Les trous
supérieurs à cinq minutes sont ignorés ; pas de recalage sur le réseau routier.

**Quel temps réel ?** Micro-lots de 20 secondes pour Silver ; Gold toutes les 2 minutes,
plus le temps réel de calcul. La fraîcheur est affichée dans le dashboard.

## Démonstration

Préparer Docker avant la soutenance, puis montrer la commande de lancement, trois
messages Kafka, les zones MinIO, le DAG réussi et Streamlit. Produire des captures
réelles de secours. Ne pas remplacer une panne par des résultats inventés.
