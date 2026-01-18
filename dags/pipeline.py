from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta   
from scrapers.pipe_talen import scrappe_talen
from scrapers.pipe_jungle import scrappe_jungle
from scrapers.pipe_france import scrappe_france
from processing.talen_clean import talen_clean
from processing.jungles_clean import jungles_clean
from processing.france_clean import france_clean
from processing.merge import merge_csv


#configuration par défaut du DAG
Base_Path = "/opt/airflow/shared_data"
default_args = {
    'owner': 'airflow',
    'retry_delay': timedelta(minutes=2),
    "start_date": datetime(2024, 1, 1)
}

#Définition du DAG
with DAG(
    dag_id = "job_scraping_pipeline",
    default_args=default_args,
    description= "pipeline pour l'orchestration pour la collecte d'offres d'emploi sur les sites de recherche d'emploi",
    schedule_interval="@daily",
    catchup=False,
) as dag:

    #Tâche 1 : Scraping des offres d'emploi sur LinkedIn
    scrape_talen_task = PythonOperator(
        task_id="scrape_talen_jobs",
        python_callable=scrappe_talen,
        op_kwargs={
            'url': "https://fr.talent.com/jobs?k=data&l=France&id=f5d5829db967",
            'output_file': f"{Base_Path}/talen_jobs.csv"
        }
    )

    #Tâche 2 : Scraping des offres d'emploi sur Welcome to the Jungle
    scrape_jungle_task = PythonOperator(
        task_id="scrape_jungle_jobs",
        python_callable=scrappe_jungle,
        op_kwargs={
            'url': "https://www.welcometothejungle.com/fr/jobs?query=Data%20Engineer&aroundQuery=France",
            'output_file': f"{Base_Path}/jungle_jobs.csv"
        }
    )

    #Tâche 3 : Scraping des offres d'emploi sur France Travail
    scrape_france_task = PythonOperator(
        task_id="scrape_france_jobs",
        python_callable=scrappe_france,
        op_kwargs={
            'url': "https://candidat.francetravail.fr/offres/recherche?lieux=01P&motsCles=data+engineer+&offresPartenaires=true&rayon=10&tri=0",
            'output_file': f"{Base_Path}/france_jobs.csv"
        }
    )
    
    #Tâche 4 : Nettoyage des données LinkedIn
    clean_talen_task = PythonOperator(
        task_id="clean_talen_data",
        python_callable=talen_clean,
        op_kwargs={
            'input_path': f"{Base_Path}/talen_jobs.csv",
            'output_path': f"{Base_Path}/talen_jobs_clean.csv"
        }
    )
    #Tâche 5 : Nettoyage des données Welcome to the Jungle
    clean_jungle_task = PythonOperator(
        task_id="clean_jungle_data",
        python_callable=jungles_clean,
        op_kwargs={
            'input_path': f"{Base_Path}/jungle_jobs.csv",
            'output_path': f"{Base_Path}/jungle_jobs_clean.csv"
        }
    )
    #Tâche 6 : Nettoyage des données France Travail
    clean_france_task = PythonOperator(
        task_id="clean_france_data",
        python_callable=france_clean,
        op_kwargs={
            'input_path': f"{Base_Path}/france_jobs.csv",
            'output_path': f"{Base_Path}/france_jobs_clean.csv"
        }
    )
    #Tâche 7 : Fusion des données nettoyées
    
    merge_task = PythonOperator(
        task_id="merge_cleaned_data",
        python_callable=merge_csv,
        op_kwargs={
            'file1': f"{Base_Path}/talen_jobs_clean.csv",
            'file2': f"{Base_Path}/jungle_jobs_clean.csv",
            'file3': f"{Base_Path}/france_jobs_clean.csv",
            'output_file': f"{Base_Path}/merged_jobs.csv"
        }
    )
    #Définir l'ordre d'exécution des tâches
    scrape_talen_task >> clean_talen_task
    scrape_jungle_task >> clean_jungle_task
    scrape_france_task >> clean_france_task

# Puis les 3 tâches de nettoyage >> merge_task
    [clean_talen_task, clean_jungle_task, clean_france_task] >> merge_task



