import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CSV_PATH = BASE_DIR / "shared_data" / "merged_jobs.csv"

def load_jobs(filters=None, page=1, limit=20):
    if not CSV_PATH.exists():
        return []

   
    df = pd.read_csv(CSV_PATH)

    # Nettoyage minimal
    df = df.dropna(subset=["offre", "entreprise"])

    # Filtres dynamiques
    if filters:
        for key, value in filters.items():
            if key in df.columns and value:
                df = df[df[key].astype(str).str.contains(value, case=False, na=False)]

    total = len(df)

    #  Pagination
    start = (page - 1) * limit
    end = start + limit
    df_page = df.iloc[start:end]

    return df_page.to_dict(orient="records"), total
