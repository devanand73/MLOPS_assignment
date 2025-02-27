# Proceed with experiment tracking using a simulated approach (without MLflow dependency)
# Logging metrics and parameters to a local file.

import json

#  experiment tracking
experiment_data = {
    "experiment_name": "Baseline Model Experiment",
    "parameters": {
        "n_estimators": 100,
        "random_state": 42
    },
    "metrics": {
        "accuracy": 1.0,
        "f1_score": 1.0,
        "precision": 1.0,
        "recall": 1.0
    },
    "artifacts": ["random_forest_model.pkl"]
}

# Save experiment data to a JSON file
with open("experiment_tracking.json", "w") as file:
    json.dump(experiment_data, file, indent=4)

"Experiment tracking data saved as experiment_tracking.json"