import json
import logging
from pathlib import Path

import dagshub
import mlflow
from mlflow import MlflowClient

# ---------------------------------------------
# Logging
# ---------------------------------------------
logger = logging.getLogger("register_model")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(handler)

# ---------------------------------------------
# MLflow
# ---------------------------------------------
dagshub.init(
    repo_owner="xlrboi",
    repo_name="delievery_time_predict",
    mlflow=True,
)

mlflow.set_tracking_uri(
    "https://dagshub.com/xlrboi/delievery_time_predict.mlflow"
)


def load_model_information(path: Path):
    with open(path) as f:
        return json.load(f)


if __name__ == "__main__":

    root_path = Path(__file__).parent.parent.parent

    run_info = load_model_information(
        root_path / "run_information.json"
    )

    model_uri = run_info["model_uri"]
    model_name = run_info["model_name"]

    model_version = mlflow.register_model(
        model_uri=model_uri,
        name=model_name,
    )

    logger.info(
        f"Registered Model Version : {model_version.version}"
    )

    client = MlflowClient()

    client.transition_model_version_stage(
        name=model_name,
        version=model_version.version,
        stage="Staging",
    )

    logger.info("Model moved to STAGING.")