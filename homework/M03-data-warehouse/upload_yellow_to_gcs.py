import os
import urllib.request
from google.cloud import storage, bigquery

# ==========================
# CONFIGURATION GOOGLE GCP
# ==========================
BUCKET_NAME = "de-zoomcamp-2026-homework-03-bucket"
DATASET = "de_zoomcamp_yellow-homework-03-dataset"
PROJECT_ID = "de-zoomcamp-2026-486014"
DESTINATION_FOLDER = "yellow"

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-"
MONTHS = [f"{i:02d}" for i in range(1, 7)]
DOWNLOAD_DIR = "./data/yellow"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ==========================
# FONCTIONS
# ==========================

def download_file(month: str) -> str:
    filename = f"yellow_tripdata_2024-{month}.parquet"
    url = f"{BASE_URL}{month}.parquet"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    if os.path.exists(filepath):
        print(f"Already downloaded: {filename}")
        return filepath

    print(f"Downloading: {url}")
    urllib.request.urlretrieve(url, filepath)
    print(f"Downloaded: {filepath}")

    return filepath


def upload_file_to_gcs(client, bucket_name: str, filepath: str):
    bucket = client.bucket(bucket_name)
    filename = os.path.basename(filepath)
    blob_path = f"{DESTINATION_FOLDER}/{filename}"
    blob = bucket.blob(blob_path)

    if blob.exists(client):
        print(f"Already in GCS: gs://{bucket_name}/{blob_path}")
        return

    print(f"⬆ Uploading {filename} to gs://{bucket_name}/{blob_path}")
    blob.upload_from_filename(filepath)
    print(f"Uploaded: gs://{bucket_name}/{blob_path}")


def create_bq_dataset(bq_client, dataset_id: str):
    """Créer le dataset BigQuery si il n'existe pas"""
    dataset_ref = bigquery.Dataset(f"{PROJECT_ID}.{dataset_id}")

    try:
        bq_client.get_dataset(dataset_ref)
        print(f"Dataset '{dataset_id}' already exists.")
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "EU"  # ou "US" selon ton choix
        bq_client.create_dataset(dataset)
        print(f"Dataset '{dataset_id}' created successfully.")


# ==========================
# MAIN
# ==========================

if __name__ == "__main__":
    # Clients GCP
    storage_client = storage.Client(project=PROJECT_ID)
    bq_client = bigquery.Client(project=PROJECT_ID)

    # Créer le dataset BigQuery
    create_bq_dataset(bq_client, DATASET)

    # Télécharger et uploader les fichiers Parquet
    for month in MONTHS:
        filepath = download_file(month)
        upload_file_to_gcs(storage_client, BUCKET_NAME, filepath)

    print("\nAll yellow taxi parquet files uploaded successfully!")
    print(f"BigQuery dataset '{DATASET}' is ready for creating external tables.")
