# Security & Compliance for MLOps

This document explains how security and compliance are implemented in the MLOps pipeline, covering **secrets management**, **container security**, **data privacy**, and **regulatory compliance**.  
Designed for simplicity and transparency.

---

## Table of Contents
1. [Key Features](#key-features)
2. [Secrets Management](#secrets-management)
3. [Container Security](#container-security)
4. [Data Privacy](#data-privacy)
5. [Compliance](#compliance)
6. [Setup Guide](#setup-guide)
7. [Deliverables](#deliverables)

---

## Key Features
- 🔒 **Secrets Management**: Secure storage of API keys/database credentials using AWS Secrets Manager.
- 🛡️ **RBAC**: Role-based access for CI/CD pipelines and Kubernetes.
- 📦 **Container Scanning**: Automated vulnerability checks with Trivy.
- 🕵️ **PII Protection**: Anonymization of sensitive data in logs and training datasets.
- 📜 **GDPR/HIPAA Compliance**: Documentation and technical safeguards.

---

## Secrets Management

### How It Works
1. **Store Secrets in AWS Secrets Manager**  
   Secrets (e.g., `DB_PASSWORD`) are encrypted and managed via AWS.  
   Example Terraform configuration:
   ```hcl
   resource "aws_secretsmanager_secret" "db_password" {
     name = "prod/db_password"
   }

  Access Secrets in Kubernetes
    Use the AWS Secrets CSI Driver to inject secrets into pods:

  CI/CD Access Control
    GitHub Actions uses OIDC to assume AWS roles without storing credentials:

2. **Container Security**
Trivy Vulnerability Scanning
GitHub Action Workflow:
Every Docker image is scanned for critical vulnerabilities.

3. **Data Privacy**
PII Handling
Anonymization in Training Data
Use Presidio to redact sensitive fields:

Log Scrubbing
Middleware in Flask to mask PII in logs:

4. **Compliance**
Regulatory Alignment
GDPR (EU):
Data anonymization for all PII.
Right to erasure via API endpoint.
HIPAA (Healthcare):
Encryption of data at rest (AWS EBS/S3) and in transit (TLS 1.2+).
Audit trails via AWS CloudTrail and Kubernetes audit logs.
Data Retention:
Training data: Encrypted and retained for 1 year.
Logs: Automatically purged after 30 days.