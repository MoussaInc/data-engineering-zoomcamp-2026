set -e

TAXI_TYPE=$1
YEAR=$2

PREFIX_URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download"

for MONTH in {1..12}; do
  FMONTH=$(printf "%02d" ${MONTH})

  FILE_NAME="${TAXI_TYPE}_tripdata_${YEAR}-${FMONTH}.csv.gz"

  LOCAL_DIR="/data/raw/${TAXI_TYPE}/${YEAR}"
  LOCAL_PATH="${LOCAL_DIR}/${FILE_NAME}"

  URL="${PREFIX_URL}/${TAXI_TYPE}/${FILE_NAME}"

  printf "\nProcessing %s...\n" ${FILE_NAME}

  mkdir -p ${LOCAL_DIR}

  # Télécharger seulement si le fichier n'existe pas
  if [ ! -f ${LOCAL_PATH} ]; then
      echo "Downloading ${FILE_NAME}..."
      wget -O ${LOCAL_PATH} ${URL}
  else
      echo "File already exists locally."
  fi
  
done