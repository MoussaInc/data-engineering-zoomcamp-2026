"""
@bruin
name: ingestion.trips
type: python
image: python:3.10-slim
connection: duckdb-default

materialization:
  type: table
  strategy: append
"""

def materialize():
    import os
    import json
    import pandas as pd
    import requests
    from io import BytesIO
    from datetime import datetime, timedelta
    from dateutil import parser

    start_date_str = os.environ.get("BRUIN_START_DATE")
    end_date_str = os.environ.get("BRUIN_END_DATE")
    vars_str = os.environ.get("BRUIN_VARS", "{}")
    taxi_types = json.loads(vars_str).get("taxi_types", ["yellow"])

    start_date = parser.parse(start_date_str)
    end_date = parser.parse(end_date_str)

    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/"
    current_date = start_date

    all_data = []

    while current_date <= end_date:
        year_month = current_date.strftime("%Y-%m")

        for taxi_type in taxi_types:
            filename = f"{taxi_type}_tripdata_{year_month}.parquet"
            url = base_url + filename

            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()

                df = pd.read_parquet(BytesIO(response.content))

                df["taxi_type"] = taxi_type
                df["ingestion_timestamp"] = datetime.now()
                df["source_file"] = filename

                all_data.append(df)

                print(f"✅ {len(df):,} lignes chargées")

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    print(f"⚠️ Fichier non trouvé : {filename}")
                else:
                    raise e

        current_date = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1)

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        return pd.DataFrame()