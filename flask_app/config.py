# flask_app/config.py

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SHARED_DATA_PATH = os.path.join(
    BASE_DIR,
    "..",
    "shared_data",
    "merged_jobs.csv"
)
