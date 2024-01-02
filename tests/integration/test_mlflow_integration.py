import pytest
from haikunator import Haikunator
import os
import json
import mlflow
from mlflow.exceptions import MlflowException

import tests.integration.config as config

# Generate a unique experiment name
haikunator = Haikunator()
experiment_name = f"tmp-int-{haikunator.haikunate()}"

@pytest.fixture(scope="module")
def mlflow_client():
    # Set the tracking URI for MLflow
    mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI)
    return mlflow.tracking.MlflowClient()

@pytest.fixture(scope="module")
def mlflow_experiment(mlflow_client):
    # Create an MLflow experiment
    experiment_id = mlflow_client.create_experiment(experiment_name)
    yield experiment_id
    # Teardown if needed

@pytest.mark.order(1)
def test_experiment_exists(mlflow_client, mlflow_experiment):
    # Verify that the experiment exists
    try:
        experiment = mlflow_client.get_experiment(mlflow_experiment)
        assert experiment.name == experiment_name
    except MlflowException:
        pytest.fail("Experiment does not exist")

@pytest.mark.order(1)
def test_model_registration_and_loading(mlflow_client, mlflow_experiment):
    with mlflow.start_run(experiment_id=mlflow_experiment) as run:
        # Log the JSON file as an artifact
        data = {"name": "Mark", "age": 30}
        model_file = "integration-model.json"  # File name to use for logging the artifact

        with open(model_file, "w") as f:
            json.dump(data, f)

        mlflow.log_artifact(model_file)

    if os.path.exists(model_file):
        os.remove(model_file)
        print(f"File '{model_file}' has been removed.")
    else:
        print(f"No file found at '{model_file}', nothing to remove.")
    # Run is finished, now download the artifact
    local_artifact_path = mlflow_client.download_artifacts(run.info.run_id, model_file)

    # Read and verify the JSON content
    with open(local_artifact_path) as f:
        downloaded_data = json.load(f)

    assert downloaded_data == data, "Downloaded JSON data does not match expected value"


@pytest.mark.order(2)
def test_experiment_deletion(mlflow_client, mlflow_experiment):
    # Delete experiment
    mlflow_client.delete_experiment(mlflow_experiment)
    # Verify that the experiment is deleted
    deleted_experiment = mlflow_client.get_experiment(mlflow_experiment)
    assert deleted_experiment.lifecycle_stage == "deleted"
