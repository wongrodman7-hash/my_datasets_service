import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
import joblib
import os

# Load dataset
dataset_url = 'https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-04-20/netflix_titles.csv'
print(f"Loading data from {dataset_url}")
df = pd.read_csv(dataset_url)

# Define features and target
target = 'type'
features = ['release_year', 'rating', 'duration', 'listed_in', 'country']

X = df[features]
y = df[target]

# Data split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1234)

# Fill missing values with most frequent
train_mode = dict(X_train.mode().iloc[0])
X_train = X_train.fillna(train_mode)

print("Train mode:", train_mode)

# Convert categoricals to numbers
encoders = {}
categorical_cols = ['rating', 'duration', 'listed_in', 'country']

for column in categorical_cols:
    le = LabelEncoder()
    X_train[column] = le.fit_transform(X_train[column].astype(str))
    encoders[column] = le

# Train Random Forest
print("Training Random Forest...")
rf = RandomForestClassifier(n_estimators=100)
rf.fit(X_train, y_train)

# Train Extra Trees
print("Training Extra Trees...")
et = ExtraTreesClassifier(n_estimators=100)
et.fit(X_train, y_train)

# Save preprocessing objects and models
research_dir = "research"
if not os.path.exists(research_dir):
    os.makedirs(research_dir)

joblib.dump(train_mode, os.path.join(research_dir, "train_mode.joblib"), compress=True)
joblib.dump(encoders, os.path.join(research_dir, "encoders.joblib"), compress=True)
joblib.dump(rf, os.path.join(research_dir, "random_forest.joblib"), compress=True)
joblib.dump(et, os.path.join(research_dir, "extra_trees.joblib"), compress=True)

print("Artifacts saved in the research directory.")
