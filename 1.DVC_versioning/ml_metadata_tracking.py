import mlflow
import dvc.api

data_version = dvc.api.get_url("data/processed")

with mlflow.start_run():
    mlflow.log_param("data_version", data_version)
    mlflow.log_artifact("data/processed.dvc")