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

The get_secret() function in fetch_secret.py is a secure way to retrieve sensitive information from AWS Secrets Manager. It takes a secret_name as input and connects to AWS's US East 1 region using boto3. The function attempts to fetch the secret value and returns it as a string if successful, or raises an error if something goes wrong. This approach keeps sensitive data like passwords and API keys secure by storing them in AWS's digital vault rather than in the source code. The function follows a clear try-except pattern to handle both successful retrievals and potential errors gracefully.

PII_mask.py is a privacy protection tool that automatically detects and masks sensitive personal information in text. It uses an Analyzer to identify private data (like names and emails) and an Anonymizer to replace them with generic labels. When given input text like "User John Doe (john@example.com) purchased item X", it transforms it to "User (<EMAIL_ADDRESS>) purchased item X". This process maintains the text's readability while ensuring personal information remains protected, making it ideal for handling customer data and document processing where privacy is essential.

This Flask middleware automatically protects sensitive password information in web applications by intercepting incoming HTTP requests. Using the @app.before_request decorator, the scrub_pii() function checks for any 'password' field in the JSON request data and replaces it with 'REDACTED'. For example, when receiving {"username": "john", "password": "secret123"}, it transforms it to {"username": "john", "password": "REDACTED"} before the request reaches the main application. This simple but powerful security measure prevents accidental exposure of passwords in logs or application processing.

Deploy.yml is a GitHub Actions workflow configuration that establishes secure AWS access for deployments using OIDC authentication. It sets up required permissions for ID token writing and content reading, then configures AWS credentials by assuming a specified role (arn:aws:iam::1234567890:role/github-actions-role) in the us-east-1 region. This creates a secure authenticated session between GitHub Actions and AWS, enabling subsequent workflow steps to safely interact with AWS services using temporary credentials. The configuration handles the security handshake where GitHub generates a token, authenticates with AWS, and receives verified access credentials.

GitHub Workflow CI Container Scanner (ci.yml) is an automated security pipeline that runs on Ubuntu and uses Trivy to scan Docker container images for vulnerabilities. It specifically checks for HIGH and CRITICAL security issues in the specified Docker image ("your-docker-image:latest") and outputs findings in a table format. The workflow will fail if serious vulnerabilities are detected (exit-code: "1"), acting as a security gate before deployment. This automated process ensures container images meet security standards before reaching production environments.

RBAC Role Definition in rbac.yml creates a security configuration in Kubernetes that defines specific access permissions within the "mlops" namespace. The Role named "deploy-role" grants three key permissions (get, list, create) specifically for working with deployments in the "apps" API group. This acts like an access card that can be assigned to users or service accounts, controlling exactly what actions they can perform on deployment resources. When combined with a RoleBinding, it enables fine-grained access control following security best practices by granting only necessary permissions.

@5.Security_compliance\K8\secrets.yml creates a SecretProviderClass in Kubernetes that securely connects to AWS Secrets Manager. It specifically configures access to retrieve a DB_PASSWORD secret from AWS, acting as a secure bridge between Kubernetes applications and sensitive data storage. When applied, this configuration enables pods to safely fetch the database password without storing it directly in application code or configuration files. The setup uses the secrets-store CSI driver to establish a secure data flow from AWS Secrets Manager to any authorized Kubernetes pods that need access to the secret.
