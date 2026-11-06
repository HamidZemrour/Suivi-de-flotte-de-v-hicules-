# Matrice de conformité au PDF

Référence : Projets_BigData_ADIA_IL_ISSE.pdf, guide général et ligne ISSE-05.
Le PDF a une pagination divisée horizontalement ; les exigences sont reprises par thème.

| Exigence | Implémentation / livrable | Vérification restante |
|---|---|---|
| Sujet 5 ISSE : suivi de flotte | simulation de 12 GPS à Casablanca | démonstration locale |
| MQTT → Kafka, topic positions | simulator.py, bridge.py, Mosquitto, 3 partitions | observer les messages |
| Bronze : positions brutes | payload et offsets en Parquet sur MinIO | vérifier les objets |
| Silver : trajets Hudi | positions nettoyées, partitions day, upsert event_id | tester une reprise et les doublons |
| Gold : distance, vitesse, incidents | gold_daily, gold_latest, gold_incidents | comparer les valeurs source/Gold |
| Streaming : géorepérage et excès | stream.py, règles à chaque micro-lot | montrer les indicateurs |
| Spark SQL : statistiques | analytics.py, agrégat journalier | comparer un calcul manuel |
| MLlib : KMeans zones d'arrêt | analytics.py, modèle et centres sauvegardés | vérifier au moins 2 centres |
| DAG quotidien rapport de conduite | daily_report.py | exécuter et ouvrir reports/ |
| Orchestration des traitements | refresh_gold.py → service Spark interne | succès dans Airflow |
| Carte flotte et incidents | Streamlit connecté aux exports Gold | capturer le dashboard |
| Docker Compose unique | docker-compose.yml | lancement complet sur le PC |
| Cahier des charges PDF | docs/Cahier_des_charges.pdf | noms du groupe |
| Code + README sur Git | dépôt GitHub et ZIP | contributions individuelles |
| Rapport final PDF | docs/Rapport_projet.pdf | ajouter résultats et captures réels |
| Présentation PDF/PPTX | docs/Presentation.pdf et .pptx | répéter la soutenance |
| Groupe de 4, comptes séparés | docs/EQUIPE.md | obligation à remplir par les étudiants |

Choix autorisés : simulation Python au lieu de GeoLife ; MinIO au lieu de HDFS ;
Streamlit au lieu de Grafana ; Hudi Copy-on-Write.
Le sujet demande une soutenance avec parole équilibrée et démonstration testée à l'avance.
Les durées et points du barème ne sont pas lisibles dans le PDF fourni ; aucune valeur
n'est inventée. La note finale indiquée est 60 % collective / 40 % individuelle.
