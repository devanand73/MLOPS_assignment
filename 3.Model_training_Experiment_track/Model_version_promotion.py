# model versioning and promotion.
# Using a local JSON file to represent a model registry

import json

# Simulated model registry
model_registry = {
    "models": [
        {
            "model_name": "random_forest_model",
            "version": 1,
            "stage": "development",
            "metrics": {
                "accuracy": 1.0,
                "f1_score": 1.0,
                "precision": 1.0,
                "recall": 1.0
            },
            "artifact": "random_forest_model.pkl"
        }
    ]
}

# Promote the model to production
for model in model_registry["models"]:
    if model["model_name"] == "random_forest_model" and model["version"] == 1:
        model["stage"] = "production"

# Save the updated model registry to a JSON file
with open("model_registry.json", "w") as file:
    json.dump(model_registry, file, indent=4)

"Model registry updated and saved as model_registry.json"