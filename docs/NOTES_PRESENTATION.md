# Notes orales

## 1. Suivi de flotte de véhicules

Présenter les quatre membres et leurs contributions réelles. Le projet utilise des données simulées, pas une flotte réelle.

## 2. Pourquoi suivre une flotte ?

Expliquer le besoin d'un gestionnaire de flotte. La limite de vitesse est une règle pédagogique de 80 km/h, sans référence aux limitations réelles de chaque route.

## 3. Le cadre du projet

Rappeler le sujet ISSE-05 du PDF. Le groupe compte obligatoirement quatre étudiants de la même filière, avec contributions Git individuelles.

## 4. Du GPS au tableau de bord

Suivre un message unique de sa production à la carte. Bronze conserve le payload d'origine. Airflow pilote le service Spark interne par HTTP, sans accès au socket Docker.

## 5. Un flux reproductible

Le débit nominal du générateur est six messages par seconde, pas une performance mesurée de la plateforme. Les positions ne sont pas recalées sur les routes.

## 6. MQTT et Kafka

Décrire pourquoi la livraison peut se répéter. Le dispositif n'annonce pas une garantie exactly-once globale. La clé véhicule conserve le regroupement des événements par véhicule dans Kafka.

## 7. Bronze, Silver, Gold

Montrer les répertoires .hoodie pendant la démo. L'index global permet le déplacement de partitions de gold_latest. Les exports JSON rendent les données Gold accessibles à Streamlit.

## 8. Détecter et mesurer

Les incidents sont des mesures, pas des épisodes regroupés. Une distance issue de points GPS échantillonnés sous-estime les trajets courbes. Montrer les règles et leurs seuils.

## 9. Découvrir les zones d’arrêt

KMeans est non supervisé, il n'a pas une accuracy de classification. Avec moins de deux points distincts, pas d'entraînement. En amélioration : silhouette et comparaison de plusieurs valeurs de k.

## 10. Airflow pilote les calculs

Montrer les deux DAG. Le streaming est un service continu Docker ; Airflow orchestre le batch et les modèles. Un rapport sans données pour la date est explicite, sans inventer un historique.

## 11. La vue du gestionnaire

Ouvrir Streamlit. La carte dépend de l'accès aux tuiles cartographiques. Le dashboard relit ses snapshots toutes les trente secondes ; Gold est calculé toutes les deux minutes, plus la durée de traitement.

## 12. Ce qui est vérifié

La construction cloud a été arrêtée par la limite de disque. Distinguer les tests effectivement exécutés et la recette locale à compléter. Ajouter des captures et résultats réels avant la soutenance.

## 13. Une preuve à chaque couche

Préparer la démonstration à l'avance. Chaque étudiant explique sa couche. Préparer des captures réelles de secours et ne pas simuler un succès technique.

## 14. Quatre responsabilités, une chaîne

Remplacer membre 1 à 4 par les noms. Décrire les contributions réelles et les commits de chaque compte. Ne pas attribuer artificiellement le code généré à quatre personnes.

## 15. Une base à valider et enrichir

Terminer sur les apprentissages : flux, lakehouse, traitement distribué, orchestration et visualisation. Ne pas annoncer le projet comme validé en production.
