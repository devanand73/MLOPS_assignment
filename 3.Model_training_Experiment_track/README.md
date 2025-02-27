
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


