# Mon Projet
Job Scraping & API Pipeline – Airflow & Flask
Description du projet

Ce projet implémente une architecture complète de collecte, traitement et exposition d’offres d’emploi Data en France.
Il combine Apache Airflow pour l’orchestration des pipelines de données et Flask pour l’exposition des données traitées via une API REST.

L’objectif est de construire une chaîne data de bout en bout :

ingestion automatisée des données,

nettoyage et consolidation,

mise à disposition des résultats pour des applications externes (dashboard, frontend, recommandations).

Architecture globale

Le projet repose sur deux composants principaux :

1. Airflow – Pipeline de données

Scraping automatisé des offres d’emploi

Nettoyage et normalisation des données

Fusion des datasets dans un fichier consolidé

2. Flask – API de données

Lecture des données produites par Airflow

Exposition des offres via des endpoints REST

Consommation possible par un frontend ou un outil de visualisation

Les deux composants partagent un volume de données commun (shared_data).

Sources de données

Les offres d’emploi sont collectées depuis :

Talent.com

Welcome to the Jungle

France Travail

Chaque source est traitée indépendamment afin d’assurer la robustesse du pipeline.

Pipeline Airflow
DAG

DAG ID : job_scraping_pipeline

Planification : quotidienne (@daily)

Catchup : désactivé

Start date : 1er janvier 2024

Étapes du pipeline

Scraping des offres pour chaque plateforme

Nettoyage des données (formats, doublons, valeurs manquantes)

Fusion des datasets nettoyés

Génération d’un fichier CSV consolidé

Les données sont stockées dans le répertoire partagé :

/opt/airflow/shared_data

API Flask

L’application Flask permet d’exposer les données générées par Airflow.

Rôles de l’API

Lecture du fichier merged_jobs.csv

Filtrage et recherche d’offres

Fourniture de données prêtes à être consommées par :

un dashboard (Power BI, Tableau),

une application web,

un moteur de recommandation.

Exemple d’usage

Récupérer la liste des offres Data Engineer

Filtrer par localisation ou mot-clé

Alimenter un frontend ou une API externe

Structure du projet
Projet1/
│── dags/
│   └── pipeline.py
│
│── scrapers/
│   ├── pipe_talen.py
│   ├── pipe_jungle.py
│   └── pipe_france.py
│
│── processing/
│   ├── talen_clean.py
│   ├── jungles_clean.py
│   ├── france_clean.py
│   └── merge.py
│
│── flask_app/
│   ├── app.py
│   └── routes/
│
│── shared_data/
│   └── merged_jobs.csv
│
│── Dockerfile
│── docker_compose.yaml
│── .gitignore
│── README.md

Technologies utilisées

Python

Apache Airflow

Flask

Docker / Docker Compose

Pandas

Web Scraping

Lancement du projet
Prérequis

Docker

Docker Compose

Démarrage
docker-compose up -d

Accès

Airflow : http://localhost:8080

API Flask : http://localhost:5000/jobs
            http://localhost:5000/Dashboard

Données de sortie

Les données consolidées sont accessibles :

sous forme de fichier CSV (shared_data/merged_jobs.csv)

via l’API Flask

Ces données peuvent être exploitées pour :

analyse du marché de l’emploi Data,

dashboards,

systèmes de recommandation,

applications web.

Bonnes pratiques

Les logs Airflow ne sont pas versionnés

Les environnements virtuels sont ignorés

Séparation claire entre orchestration (Airflow) et exposition (Flask)

Perspectives d’évolution

Authentification sur l’API Flask

Stockage en base de données (PostgreSQL)

Ajout de nouvelles sources d’offres

Dashboard interactif

Recommandation intelligente d’offres

Auteur

Yankam Pegmi Frank Jores

Projet orienté Data Engineering, orchestration de pipelines et API data.

