import pandas as pd

def merge_csv(file1, file2, file3, output_file):
    # Lire les fichiers CSV
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    df3 = pd.read_csv(file3)
    
    # Concaténer les DataFrames
    merged_df = pd.concat([df1, df2, df3], ignore_index=True)
    
    merged_df.drop_duplicates(subset=['offre', 'entreprise'],inplace=True)

    merged_df.reset_index(drop=True, inplace=True)
    # Enregistrer le DataFrame fusionné dans un nouveau fichier CSV
    merged_df.to_csv(output_file, index=False)