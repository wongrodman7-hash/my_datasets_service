from django.apps import AppConfig
import inspect
import os

class MlConfig(AppConfig):
    name = 'apps.ml'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true': # Ensure it only runs once with runserver
            from apps.ml.registry import registry
            from apps.ml.movie_classifier.random_forest import RandomForestClassifier
            
            try:
                print("Initializing ML registry...")
                # Random Forest classifier
                rf = RandomForestClassifier()
                # add to ML registry
                registry.add_algorithm(endpoint_name="movie_classifier",
                                        algorithm_object=rf,
                                        algorithm_name="random forest",
                                        algorithm_status="production",
                                        algorithm_version="0.0.1",
                                        owner="Piotr",
                                        algorithm_description="Random Forest with simple pre- and post-processing",
                                        algorithm_code=inspect.getsource(RandomForestClassifier))
                print(f"ML registry initialized. Endpoints: {list(registry.endpoints.keys())}")
            except Exception as e:
                print("Exception while loading the algorithms to the registry,", str(e))
