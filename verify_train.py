import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

print(f"Current working directory: {os.getcwd()}")

if not os.path.exists('research'):
    print("Creating research directory...")
    os.makedirs('research')

dataset_url = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-04-20/netflix_titles.csv'
print(f"Loading data from {dataset_url}")
df = pd.read_csv(dataset_url)

print("Preprocessing...")
X = df[['release_year']] # Simple feature for verification
y = df['type']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1234)

rf = RandomForestClassifier(n_estimators=10)
rf.fit(X_train, y_train)

save_path = os.path.join("research", "random_forest.joblib")
print(f"Saving model to {save_path}")
joblib.dump(rf, save_path)

if os.path.exists(save_path):
    print("Model saved successfully!")
else:
    print("Failed to save model.")
