import requests
import pandas as pd
import json

# URL of the prediction endpoint
url = "http://localhost:8000/api/v1/movie_classifier/predict"

# Sample data from Netflix titles (top movies/shows)
# Usually we would load the CSV, but for a quick demo script, I'll hardcode a few real examples
# from the dataset format.

test_data = [
    {
        "title": "Dick Johnson Is Dead",
        "data": {
            "release_year": 2020,
            "rating": "PG-13",
            "duration": "90 min",
            "listed_in": "Documentaries",
            "country": "United States"
        }
    },
    {
        "title": "Blood & Water",
        "data": {
            "release_year": 2021,
            "rating": "TV-MA",
            "duration": "2 Seasons",
            "listed_in": "International TV Shows, TV Dramas, TV Mysteries",
            "country": "South Africa"
        }
    },
    {
        "title": "Squid Game",
        "data": {
            "release_year": 2021,
            "rating": "TV-MA",
            "duration": "1 Season",
            "listed_in": "International TV Shows, TV Dramas, TV Thrillers",
            "country": "South Korea"
        }
    }
]

print("--- Netflix Movie/TV Show Predictor ---")
print(f"Connecting to: {url}\n")

for item in test_data:
    print(f"Predicting type for: {item['title']}")
    try:
        response = requests.post(url, json=item['data'])
        if response.status_code == 200:
            result = response.json()
            print(f"  Prediction: {result['label']}")
            print(f"  Probability: {result['probability']:.2f}")
            print(f"  Request ID: {result['request_id']}")
        else:
            print(f"  Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"  Failed to connect to server: {e}")
    print("-" * 40)
