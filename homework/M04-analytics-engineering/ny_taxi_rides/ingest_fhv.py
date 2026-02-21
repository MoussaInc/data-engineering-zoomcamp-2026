import requests, os
from pathlib import Path
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()
PROJECT_ID = os.getenv("PROJECT_ID")
DATASET_ID = os.getenv("DATASET_ID")
TABLE_ID   = os.getenv("TABLE_ID")

BASE_URL   = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv"

data_dir = Path("data/fhv")
data_dir.mkdir(parents=True, exist_ok=True)

# Schéma fixe pour éviter les conflits de types entre mois
SCHEMA = [
    bigquery.SchemaField("dispatching_base_num",  "STRING"),
    bigquery.SchemaField("pickup_datetime",        "TIMESTAMP"),
    bigquery.SchemaField("dropOff_datetime",       "TIMESTAMP"),
    bigquery.SchemaField("PUlocationID",           "int64"),
    bigquery.SchemaField("DOlocationID",           "int64"),
    bigquery.SchemaField("SR_Flag",                "STRING"),
    bigquery.SchemaField("Affiliated_base_number", "STRING"),
]

client = bigquery.Client(project=PROJECT_ID)

for month in range(1, 13):
    filename = f"fhv_tripdata_2019-{month:02d}.csv.gz"
    filepath = data_dir / filename

    # Téléchargement (skip si déjà présent)
    if not filepath.exists():
        print(f"Téléchargement {filename}...")
        response = requests.get(f"{BASE_URL}/{filename}", stream=True)
        response.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    else:
        print(f"Skipping {filename} (déjà téléchargé)")

    # Chargement dans BigQuery
    print(f"Chargement dans BigQuery...")
    with open(filepath, "rb") as f:
        job = client.load_table_from_file(
            f,
            f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}",
            job_config=bigquery.LoadJobConfig(
                schema=SCHEMA,
                source_format=bigquery.SourceFormat.CSV,
                write_disposition="WRITE_APPEND",
                skip_leading_rows=1,
                autodetect=False,
            ),
        )
        job.result()

    print(f"✓ Mois {month:02d} chargé")
    filepath.unlink()  # supprime le fichier local pour économiser l'espace

print(f"\nIngestion terminée → {PROJECT_ID}.{DATASET_ID}.{TABLE_ID}")