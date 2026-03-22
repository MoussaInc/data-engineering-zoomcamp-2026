import dlt
import requests
from typing import Iterator, Dict, Any
import duckdb

BASE_URL = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"


def fetch_taxi_data() -> Iterator[Dict[str, Any]]:
    """
    Fetch NYC taxi data from paginated API
    """
    page = 1

    while True:
        print(f"\n\t Fetching page {page}...")

        response = requests.get(f"{BASE_URL}?page={page}")
        response.raise_for_status()
        data = response.json()

        if not data:
            print(f"\n\t Reached empty page. Total pages: {page - 1}")
            break

        print(f"\n\t Retrieved {len(data)} records from page: {page}")

        yield data

        page += 1


@dlt.resource(name="taxi_trips", write_disposition="replace")
def taxi_trips_resource():
    yield from fetch_taxi_data()


def run_pipeline():
    pipeline = dlt.pipeline(
        pipeline_name="nyc_taxi_pipeline",
        destination="duckdb",
        dataset_name="nyc_taxi_data",
        dev_mode=False
    )

    print("\n\t Starting pipeline...")
    load_info = pipeline.run(taxi_trips_resource())

    print("\n\t Pipeline completed!")
    print(f"\n\t Dataset: {load_info.dataset_name}")
    #print(f"\n\t Tables: {list(load_info.load_packages[0].schema_update.keys())}")
    pipeline = dlt.attach("nyc_taxi_pipeline")
    dataset = pipeline.dataset()
    print(f"\n\t Tables: {dataset.tables}")
    

    return pipeline, load_info


def analyze_data():

    con = duckdb.connect("nyc_taxi_pipeline.duckdb")

    stats = con.execute("""
        SELECT 
            COUNT(*) as total_trips,
            MIN(trip_pickup_date_time) as earliest_trip,
            MAX(trip_pickup_date_time) as latest_trip,
            ROUND(AVG(fare_amt), 2) as avg_fare,
            ROUND(AVG(trip_distance), 2) as avg_distance,
            SUM(total_amt) as total_revenue
        FROM nyc_taxi_data.taxi_trips
    """).fetchdf()

    print("\n\t NYC Taxi Statistics:")
    print(stats.to_string(index=False))

    con.close()


if __name__ == "__main__":
    pipeline, load_info = run_pipeline()
    analyze_data()