# Implementing baseline model training and logging to MLflow
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import mlflow
import mlflow.sklearn
import joblib

# Load a sample dataset (Iris dataset for demonstration)
from sklearn.datasets import load_iris
data = load_iris()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a baseline model (Random Forest)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average='weighted')
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')

# Save the model locally
joblib.dump(model, "random_forest_model.pkl")

# Output metrics
metrics = {
    "accuracy": accuracy,
    "f1_score": f1,
    "precision": precision,
    "recall": recall
}

metrics

# Log metrics and model to MLflow
mlflow.set_tracking_uri("http://localhost:5000")  # Replace with your MLflow server URI
mlflow.set_experiment("Baseline Model Experiment")

with mlflow.start_run():
    # Log parameters
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("random_state", 42)

    # Log metrics
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("f1_score", f1)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)

    # Log the model
    mlflow.sklearn.log_model(model, "random_forest_model")

    print("Baseline model training and logging complete.")