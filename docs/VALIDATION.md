# Journal de validation — 6 novembre 2026

## Exécuté avec succès

- `python -m unittest discover -s tests -v` : 2 tests, succès ; distance connue,
  coordonnées identiques, seuil d'excès 80/81, sortie de zone et valeurs invalides.
- `python -m compileall -q app jobs dags` : succès.
- `docker compose config -q` : succès.

- Recette Spark 3.5.3 locale : `SPARK_SMOKE_OK`. Transformations réelles testées :
  rejet invalide, dédoublonnage, seuils, Haversine, agrégation SQL et KMeans à 2 centres.

- Recette Hudi 0.15.0 locale : `HUDI_SMOKE_OK`. Deux écritures de la même clé
  conservent une ligne et mettent à jour la vitesse et l'alerte. Test sur disque local,
  pas sur MinIO ; le transport S3A reste à valider dans la recette Docker.

## Tentative d'intégration

Construction Docker lancée avec la chaîne de confiance CA du proxy cloud.
Les images de base ont pu être téléchargées et boto3 installé dans l'image Spark.
La construction s'est arrêtée avec `no space left on device` dans le stockage Docker
VFS de l'environnement cloud (volume de 8 Go). Aucune démonstration complète n'a été
validée et aucun chiffre de performance n'est revendiqué.

## Recette à exécuter sur le PC

| Contrôle | Résultat observé / date |
|---|---|
| `docker compose up --build -d` et services stables | À compléter |
| topic positions reçoit des JSON | À compléter |
| Bronze contient payload et offsets | À compléter |
| Silver comporte .hoodie et pas de doublons event_id | À compléter |
| rafraîchissement Gold réussit dans Airflow | À compléter |
| distance/vitesse cohérentes pour un véhicule | À compléter |
| carte, incidents et CSV visibles | À compléter |
| centres KMeans et modèle sauvegardés | À compléter |
| rapport quotidien sauvegardé | À compléter |
| redémarrage sans effacer volumes puis reprise | À compléter |

En cas de panne : `docker compose logs --tail=100 NOM_SERVICE`.
Maven : vérifier Internet et les certificats ; ne pas désactiver TLS.
Échec initial avant création Silver : attendre le premier micro-lot puis relancer le DAG.
Mémoire insuffisante : augmenter la mémoire attribuée à Docker Desktop.
