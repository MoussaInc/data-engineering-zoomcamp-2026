#!/usr/bin/env bash

set -e

TAXI_TYPE=$1   # Expects "yellow", "green", or "fhv"
YEAR=$2        # Expects : 2020 or 2021

PREFIX_URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download"
BUCKET="gs://de-zoomcamp-2026-homework-07-bucket"

if [ -z "$TAXI_TYPE" ] || [ -z "$YEAR" ]; then
  echo "Usage: $0 <taxi_type> <year>"
  echo "Example: $0 yellow 2020"
  exit 1
fi

for MONTH in {1..12}; do
  FMONTH=$(printf "%02d" ${MONTH})

  FILE_NAME="${TAXI_TYPE}_tripdata_${YEAR}-${FMONTH}.csv.gz"
  
  URL="${PREFIX_URL}/${TAXI_TYPE}/${FILE_NAME}"

  DESTINATION="${BUCKET}/raw/${TAXI_TYPE}/${YEAR}/${FILE_NAME}"

  echo "-----------------------------------------"
  echo "Processing ${FILE_NAME}"
  echo "Source: ${URL}"
  echo "Destination: ${DESTINATION}"

  wget -qO- ${URL} | gsutil cp - ${DESTINATION}

  echo "Upload completed"

done

echo "All files processed"