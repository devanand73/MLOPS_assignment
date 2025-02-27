# MLOps Deployment & CI/CD Pipeline

This repository implements a robust MLOps pipeline for deploying machine learning models with **containerization**, **CI/CD automation**, **staging/production environments**, and **Infrastructure as Code (IaC)**. Below is a simplified guide to the implementation.

---

## Table of Contents
1. [Overview](#overview)
2. [Key Components](#key-components)
3. [Prerequisites](#prerequisites)
4. [Getting Started](#getting-started)
5. [CI/CD Pipeline](#cicd-pipeline)
6. [Deployment Strategies](#deployment-strategies)
7. [Infrastructure as Code (IaC)](#infrastructure-as-code-iac)
8. [Conclusion](#conclusion)

---

## Overview
This project automates the deployment of an ML model serving API (Flask/FastAPI) using:
- **Docker** for containerization.
- **GitHub Actions** for CI/CD.
- **AWS EKS** (Kubernetes) for orchestration.
- **Terraform** for provisioning AWS infrastructure.
- **Canary** and **Blue/Green** strategies for production releases.

---

## Key Components

| Component               | Description                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| `Dockerfile`            | Containerizes the model serving application.                               |
| `.github/workflows/`    | GitHub Actions workflows for CI/CD.                                         |
| `terraform/`            | Terraform files to provision AWS EKS, VPC, IAM, and Kubernetes resources.  |
| `k8s/`                  | Kubernetes manifests for deployments, services, and configs.               |

---

## Prerequisites
1. **AWS Account** with IAM permissions for EKS, VPC, and EC2.
2. **Terraform** installed locally.
3. **Docker** and **Docker Hub** account (or AWS ECR).
4. **kubectl** and **awscli** configured.
5. GitHub repository with Actions enabled.

---



2. Containerize the Model

Build the Docker image
# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]

Build and push:
docker build -t your-dockerhub-username/mlops-app:latest .
docker push your-dockerhub-username/mlops-app:latest

3. Set Up AWS Infrastructure with Terraform
    Navigate to the terraform/ directory.

    terraform init
    terraform plan
    terraform apply

4. CI/CD Pipeline
GitHub Actions Workflows
Two workflows automate the process:

CI Pipeline: Runs on every commit to main.
Linting (flake8, black).
Unit/Integration tests (pytest).
Builds and pushes the Docker image.
CD Pipeline: Deploys to AWS EKS after CI passes.
Deploys to staging with smoke tests.
Supports canary/blue-green production releases.

5. Deployment Strategies
Staging Environment
Automatically deployed on successful CI.

Production Strategies
Canary Release:
Deploy new version to 10% of traffic.
Monitor metrics, then scale up.
Blue/Green:
Deploy new version alongside old.
Switch traffic after validation.

Conclusion
This implementation provides:

Automated testing and deployment via GitHub Actions.
Scalable AWS infrastructure managed through Terraform.
Zero-downtime deployments using canary/blue-green strategies.
Reproducible environments from development to production.