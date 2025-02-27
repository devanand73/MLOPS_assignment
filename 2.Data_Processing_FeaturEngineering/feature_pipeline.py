# File: feature_pipeline.py
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_selection import SelectKBest, f_classif
import joblib
import mlflow
import boto3
from datetime import datetime

class FeaturePipeline:
    def __init__(self, config):
        self.config = config
        self.s3 = boto3.client('s3')
        self._create_pipeline()

    def _create_pipeline(self):
        # Numerical features pipeline
        numerical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])

        # Categorical features pipeline
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        # Combine pipelines
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, self.config['numerical_features']),
                ('cat', categorical_transformer, self.config['categorical_features'])
            ])

        # Full pipeline with feature selection
        self.pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('feature_selection', SelectKBest(score_func=f_classif, k='all'))
        ])

    def run(self, data_path):
        # Load data
        df = pd.read_parquet(data_path)

        # Fit and transform
        processed_data = self.pipeline.fit_transform(df, df[self.config['target']])

        # Save artifacts
        self._save_artifacts(processed_data, df)
        return processed_data

    def _save_artifacts(self, data, raw_df):
        # Save transformed features
        output_path = f"s3://{self.config['output_bucket']}/v{self.config['version']}/features_{datetime.now().isoformat()}.parquet"
        pd.DataFrame(data).to_parquet(output_path)

        # Save pipeline model
        joblib.dump(self.pipeline, 'model/pipeline.joblib')

        # Log with MLflow
        mlflow.log_artifact('model/pipeline.joblib')
        mlflow.log_param("pipeline_version", self.config['version'])