import abc
import mlflow

from veho_ml.config import config


class VehoArtifactRegistry(abc.ABC):
    @abc.abstractmethod
    def register_artifacts(self):
        """Method that must be implemented in a subclass"""
        pass


class VehoMLFlowArtifact(VehoArtifactRegistry):
    def __init__(self):
        mlflow.set_tracking_uri(config.mlflow_tracking_uri)
