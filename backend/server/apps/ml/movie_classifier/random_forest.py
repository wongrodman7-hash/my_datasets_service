import joblib
import pandas as pd
import os

class RandomForestClassifier:
    def __init__(self):
        # Path should be relative to where manage.py is (backend/server/)
        path_to_artifacts = "../../research/"
        self.values_fill_missing = joblib.load(path_to_artifacts + "train_mode.joblib")
        self.encoders = joblib.load(path_to_artifacts + "encoders.joblib")
        self.model = joblib.load(path_to_artifacts + "random_forest.joblib")

    def preprocessing(self, input_data):
        # JSON to pandas DataFrame
        input_data = pd.DataFrame(input_data, index=[0])
        # fill missing values
        input_data = input_data.fillna(self.values_fill_missing)
        
        # convert categoricals
        for column in ["rating", "duration", "listed_in", "country"]:
            categorical_convert = self.encoders[column]
            # Handle possible missing columns or unexpected data types
            if column in input_data.columns:
                input_data[column] = categorical_convert.transform(input_data[column].astype(str))

        # Ensure correct column order
        expected_columns = ['release_year', 'rating', 'duration', 'listed_in', 'country']
        input_data = input_data[expected_columns]

        return input_data

    def predict(self, input_data):
        return self.model.predict_proba(input_data)

    def postprocessing(self, prediction):
        # prediction is probabilities for classes. 
        # The model was trained on ['Movie', 'TV Show'] (sorted order)
        # prediction[0] is probability of 'Movie'
        # prediction[1] is probability of 'TV Show'
        
        label = "Movie"
        if prediction[1] > 0.5:
            label = "TV Show"
            
        return {"probability": prediction[1], "label": label, "status": "OK"}

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)[0]  # only one sample
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction
