from django.test import TestCase
from rest_framework.test import APIClient
from apps.ml.registry import registry
from apps.ml.movie_classifier.random_forest import RandomForestClassifier
import inspect

class EndpointTests(TestCase):

    def setUp(self):
        # Register the algorithm for tests
        algorithm_object = RandomForestClassifier()
        algorithm_name = "random forest"
        algorithm_status = "production"
        algorithm_version = "0.0.1"
        algorithm_owner = "Piotr"
        algorithm_description = "Random Forest with simple pre- and post-processing"
        algorithm_code = inspect.getsource(RandomForestClassifier)
        
        registry.add_algorithm(
            endpoint_name="movie_classifier",
            algorithm_object=algorithm_object,
            algorithm_name=algorithm_name,
            algorithm_status=algorithm_status,
            algorithm_version=algorithm_version,
            owner=algorithm_owner,
            algorithm_description=algorithm_description,
            algorithm_code=algorithm_code
        )

    def test_predict_view(self):
        client = APIClient()
        input_data = {
            "release_year": 2016,
            "rating": "TV-MA",
            "duration": "93 min",
            "listed_in": "Dramas, International Movies",
            "country": "Mexico"
        }
        classifier_url = "/api/v1/movie_classifier/predict"
        response = client.post(classifier_url, input_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["label"], "Movie")
        self.assertTrue("request_id" in response.data)
        self.assertTrue("status" in response.data)
