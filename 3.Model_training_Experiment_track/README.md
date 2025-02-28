
# ML Model Training and Experiment Tracking

This project demonstrates the implementation of a machine learning pipeline with the following features:

1. **Baseline Model Training**
   - A Random Forest model was trained on the Iris dataset.
   - Metrics such as accuracy, F1-score, precision, and recall were calculated.
   - The trained model was saved as `random_forest_model.pkl`.

2. **Experiment Tracking**
   - Experiment details, including parameters, metrics, and artifacts, were logged.
   - The experiment tracking data is saved in `experiment_tracking.json`.

3. **Model Versioning**
   - A  model registry was created to track model versions and stages.
   - The model was promoted from the `development` stage to the `production` stage.
   - The model registry is saved in `model_registry.json`.

4. **CI/CD Pipeline**
   - A CI/CD pipeline was configured using GitHub Actions.
   - The pipeline automates the following steps:
     - Code checkout
     - Environment setup
     - Model training
     - Model promotion to production
   - The pipeline configuration is saved in `ci_cd_pipeline_final.yml`.




## Requirements

- Python 3.9 or higher
- Required Python libraries:
  - `scikit-learn`
  - `joblib`
  - `mlflow`


Model Training and Experiment Tracking Code (model_train_Exp_track.py) implements a machine learning pipeline using the Iris flower dataset. It loads and organizes flower measurements into training (80%) and testing (20%) sets, then trains a Random Forest model to classify different iris flower types. The code transforms raw flower measurements into predictions and evaluates the model's performance using multiple metrics (accuracy, f1-score). The entire process is automated and structured to provide clear insights into how well the model can recognize different flower types based on their measurements.


Model Version Registry Definition (Model_version_promotion.py) creates a structured dictionary called model_registry that serves as a database for tracking machine learning models. It stores essential information about a "random_forest_model" including its version (1), development stage, performance metrics (all set to 1.0), and the model's file location (random_forest_model.pkl). The nested dictionary structure makes it easy to manage multiple models, track versions, and access specific information through simple key navigation. This registry acts as a central system for monitoring and managing machine learning models throughout their development and production lifecycle.

track_Exp_Log_metrics.py creates a structured dictionary experiment_data that acts as a detailed log for machine learning experiments. It organizes information into four key sections: experiment name, model parameters (like n_estimators=100), performance metrics (accuracy, f1_score, etc.), and generated files (artifacts). The dictionary uses a nested structure to hierarchically organize this information, making it easy to track and compare different experiments. This data structure is designed to be saved as a JSON file, serving as a permanent record of experiment results and configurations.

CI/CD Pipeline for ML Model Training (ci_cd_pipeline_final.yml) is an automated workflow that executes on Ubuntu whenever code is pushed to the main branch. It performs a sequence of operations: checking out code, setting up Python 3.9, installing dependencies from requirements.txt, training a machine learning model via model_train_Exp_track.py, and promoting the successful model to production using Model_version_promotion.py. The pipeline ensures consistent and reliable model deployment by requiring each step to complete successfully before moving to the next, transforming code changes into deployed models without manual intervention.


