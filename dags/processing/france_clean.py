import pandas as pd 
import numpy as np 


def france_clean(input_path, output_path):
    df= pd.read_csv(input_path) 

    df['lien de description']=  "https://candidat.francetravail.fr"+ df['lien de description']

    df.loc[df['entreprise'].str.strip().str.match(r'^\d+$', na=False), 'adresse'] =df.loc[df['entreprise'].str.strip().str.match(r'^\d+$', na=False), 'entreprise']+'-'+ df['adresse']

    df.loc[df['entreprise'].str.strip().str.match(r'^\d+$', na=False), 'entreprise']='Autre'
    
    # Supprimer les doublons uniquement selon le lien de l'offre
    df.drop_duplicates(subset=['lien de description'], inplace=True)
    # Réinitialiser les index
    df.reset_index(drop=True, inplace=True)


    df.to_csv(output_path, index=False)
    

