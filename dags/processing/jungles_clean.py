import pandas as pd

def jungles_clean(input_path, output_path):
    
    df= pd.read_csv(input_path)
    df['lien de description']=  "https://www.welcometothejungle.com"+ df['lien de description']
     # Supprimer les doublons uniquement selon le lien de l'offre
    df.drop_duplicates(subset=['lien de description'], inplace=True)
    # Réinitialiser les index
    df.reset_index(drop=True, inplace=True)

    df.to_csv(output_path, index=False)