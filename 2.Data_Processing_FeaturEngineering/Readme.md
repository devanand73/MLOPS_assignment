# MLOps Feature Engineering Pipeline

[![CI/CD Pipeline](https://github.com/your-org/feature-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/feature-pipeline/actions)
[![Docker Image](https://img.shields.io/docker/v/your-org/feature-pipeline/latest)](https://hub.docker.com/r/your-org/feature-pipeline)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A production-ready pipeline for transforming raw data into model-ready features. Designed for MLOps workflows with built-in reproducibility and testing.

## 📌 Overview

Converts raw logs/clickstream data into ML features through:
- Automated data validation
- Missing value handling
- Feature normalization/encoding
- Versioned output storage

![Pipeline Architecture](https://raw.githubusercontent.com/your-org/feature-pipeline/main/docs/architecture.png)

## ✨ Key Features
- **Containerized Execution** (Docker)
- **CI/CD Integration** (GitHub Actions)
- **Version Control** (DVC + MLflow)
- **Automated Testing** (pytest)
- **Cloud-Native** (S3/AWS compatible)

## 🛠 Requirements
- Python 3.9+
- Docker 20.10+
- AWS account (for cloud storage)
- Git + DVC (for version control)

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/your-org/feature-pipeline.git
cd feature-pipeline

2. Install Dependencies
    pip install -r requirements.txt

3.  Build Docker Image
    docker build -t feature-pipeline .

4.  Run Pipeline Locally
# With local data
docker run -v $(pwd)/data:/data feature-pipeline run /data/input.parquet

# With cloud data
docker run -e AWS_ACCESS_KEY_ID=your_key -e AWS_SECRET_ACCESS_KEY=your_secret \
  feature-pipeline run s3://your-bucket/raw-data/input.parquet

# Feature Pipeline Documentation

## Dockerfile

Dockerfile creates a containerized environment for data processing tasks using Python 3.9. It sets up all necessary dependencies from requirements.txt, configures AWS and MLflow credentials, and provides two execution modes: running the feature pipeline with "--local-run" or executing tests via pytest. The container ensures consistent execution across different systems by packaging all code, dependencies, and configurations in a standardized environment. This setup streamlines both development and testing workflows while maintaining all required tools and settings in one portable container.

## feature_pipeline.py
Feature Pipeline (feature_pipeline.py) is a data processing system that automates the preparation of numerical and categorical data for machine learning. It takes a configuration dictionary and raw data as input, then processes them through two specialized paths: numerical data gets median imputation and scaling, while categorical data receives most frequent value imputation and one-hot encoding. The pipeline leverages scikit-learn components to create a reusable transformation workflow that outputs cleaned, machine-learning-ready data while integrating with cloud services (AWS) and MLflow for tracking. This standardized approach ensures consistent data preparation.

## test_pipeline.py
sample_data() fixture function in test_pipeline.py

This fixture function creates a small test dataset as a pandas DataFrame with three columns: 'num_feat' (numeric values with one missing), 'cat_feat' (categorical values with one missing), and 'target' (binary values 0/1). The data is structured to include both normal cases and edge cases like missing values (np.nan and None), making it perfect for testing data processing functions. The function takes no inputs and returns a consistent DataFrame that can be reused across multiple test cases, helping ensure reliable and repeatable tests.

## ci.yml
Feature Pipeline CI Test Job defines an automated testing environment using a Docker container running on Ubuntu. It authenticates using DockerHub credentials stored as GitHub secrets, then executes pytest commands on the test files. The job provides an isolated, consistent testing environment by using the my-feature-pipeline:latest Docker image, ensuring reliable test execution. If any test fails, the entire job fails, maintaining code quality standards before changes can be merged or deployed.

## Kubernetes CronJob Template (cronjob.yml)

This template defines how to run an automated data processing job in Kubernetes. It uses a container image "my-feature-pipeline:latest" and runs with the "--hourly-run" argument to perform scheduled data processing tasks. The template creates a structured way to execute the feature pipeline job consistently, specifying exactly what container to run and how to handle failures through the OnFailure restart policy. Think of it as a precise recipe that Kubernetes follows to ensure your data processing job runs reliably on schedule.



. Testing
# Run all tests
pytest tests/

# Test specific component
pytest tests/test_data_validation.py

# Run tests in Docker
docker run feature-pipeline pytest tests/

6.  Version Control
# Track code changes
git add .
git commit -m "Added new feature transformer"

# Track data artifacts
dvc add data/processed_features.parquet
dvc push

# Track ML experiments
mlflow ui

7.  Sample Output
Processed features are stored with versioning:

s3://your-feature-bucket/
└── v1.0/
    ├── features_2024-01-01T12:00:00.parquet
    └── features_2024-01-01T13:00:00.parquet

8.  CI/CD Pipeline
Automatically triggers on:
Code commits
Pull requests
Manual triggers

Performs:
Unit/integration tests
Docker image build
Vulnerability scanning
Deployment to staging
