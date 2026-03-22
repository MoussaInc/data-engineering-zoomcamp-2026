import requests

url = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"
res = requests.get(url)
data = res.json()
print(f"Taille de data: \t {len(data)}")
print(f"Lecture 1iere ligne : \n {data[0]}")
print(f"Lecture derniere ligne : \n {data[-1]}")