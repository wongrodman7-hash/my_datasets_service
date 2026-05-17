from apps.endpoints.models import Endpoint
from apps.endpoints.models import MLAlgorithm
from apps.endpoints.models import MLAlgorithmStatus

class MLRegistry:
    def __init__(self):
        self.endpoints = {}

    def add_algorithm(self, endpoint_name, algorithm_object, algorithm_name,
                    algorithm_status, algorithm_version, owner,
                    algorithm_description, algorithm_code):
        # get endpoint
        endpoint, _ = Endpoint.objects.get_or_create(name=endpoint_name, owner=owner)

        # get algorithm
        database_object, algorithm_created = MLAlgorithm.objects.get_or_create(
                name=algorithm_name,
                description=algorithm_description,
                code=algorithm_code,
                version=algorithm_version,
                owner=owner,
                parent_endpoint=endpoint)
        
        if algorithm_created:
            status = MLAlgorithmStatus(status = algorithm_status,
                                        created_by = owner,
                                        parent_mlalgorithm = database_object,
                                        active = True)
            status.save()
        
        # Ensure the status is active for this algorithm
        status = MLAlgorithmStatus.objects.filter(parent_mlalgorithm=database_object, active=True)
        if not status.exists():
            # Create a new active status if none exists
            MLAlgorithmStatus.objects.create(status = algorithm_status,
                                            created_by = owner,
                                            parent_mlalgorithm = database_object,
                                            active = True)

        # Deactivate other algorithms for this endpoint
        other_statuses = MLAlgorithmStatus.objects.filter(
            parent_mlalgorithm__parent_endpoint=endpoint,
            active=True
        ).exclude(parent_mlalgorithm=database_object)
        
        for s in other_statuses:
            s.active = False
            s.save()

        # add to registry
        self.endpoints[database_object.id] = algorithm_object

# Global registry instance
registry = MLRegistry()
