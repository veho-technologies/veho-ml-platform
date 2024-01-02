import abc
import mlflow

from config import config


class VehoArtifactRegistry(abc.ABC):
    def __init__(self):
        mlflow.set_tracking_uri(config.mlflow_tracking_uri)
        self.mlflow_client = mlflow.MlflowClient()
        
    @abc.abstractmethod
    def register_artifacts(self):
        """Method that must be implemented in a subclass"""
        pass


class VehoMLFlowArtifact(VehoArtifactRegistry):
    def __init__(self):
        mlflow.set_tracking_uri(config.mlflow_tracking_uri)
