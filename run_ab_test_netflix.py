import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import requests
import time

# load dataset
dataset_url = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-04-20/netflix_titles.csv'
df = pd.read_csv(dataset_url)

# Define features and target
target_col = 'type'
features = ['release_year', 'rating', 'duration', 'listed_in', 'country']

X = df[features]
y = df[target_col]

# data split train / test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1234)

print(f"Total test rows available: {len(X_test)}")

# Using first 20 rows for a quick A/B test simulation
num_iterations = 20

print(f"Starting A/B test simulation for {num_iterations} iterations...")

for i in range(num_iterations):
    # Convert numpy types to native Python types for JSON serialization
    input_row = X_test.iloc[i].fillna("")
    input_data = {}
    for col, val in input_row.items():
        if isinstance(val, (np.int64, np.int32, np.int16, np.int8)):
            input_data[col] = int(val)
        elif isinstance(val, (np.float64, np.float32)):
            input_data[col] = float(val)
        else:
            input_data[col] = val
            
    target = y_test.iloc[i]
    
    # Send prediction request
    try:
        r = requests.post("http://127.0.0.1:8000/api/v1/movie_classifier/predict?status=ab_testing", json=input_data)
        if r.status_code != 200:
            print(f"Iteration {i}: Prediction Error - {r.text}")
            continue
            
        response = r.json()
        if "label" not in response:
            print(f"Iteration {i}: API Response missing 'label' - {response}")
            continue
            
        request_id = response["request_id"]
        
        # Provide feedback with true label
        # Feedback is sent as a PUT request to the specific MLRequest object
        f = requests.put(f"http://127.0.0.1:8000/api/v1/mlrequests/{request_id}", json={"feedback": target})
        
        if f.status_code == 200:
            print(f"Iteration {i}: Success. Request ID: {request_id}, Predicted: {response['label']}, Actual: {target}")
        else:
            print(f"Iteration {i}: Feedback Error - {f.text}")
            
    except Exception as e:
        print(f"Iteration {i}: Connection Error - {e}")
        break

print("\nA/B test simulation completed.")
print("You can now check the results in the database and stop the test via API.")
