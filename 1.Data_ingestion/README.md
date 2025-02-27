# Data Ingestion Pipeline Stage Documentation

---

## **Stage Overview**
This stage establishes an **automated, versioned data ingestion pipeline** for structured MLOps workflows. Built on AWS, it enforces data integrity, auditability, and infrastructure-as-code practices.

### **Key Components**
1. **Infrastructure Foundation** (`Data_ingestion_stack.py`)  
   Creates S3 buckets (raw/processed/quarantined data), DynamoDB tracking, and notifications for traceable data flow.

2. **Orchestration** (`lambda_function.py`)  
   AWS Lambda triggers SageMaker jobs for new data, tracks state via DynamoDB, and enforces bucket isolation.

3. **Data Validation** (`process.py`)  
   Validates schema compliance (columns, data types) and auto-fixes inconsistencies (e.g., missing fields).

4. **CI/CD Automation** (`deploy.yml`)  
   GitHub Actions workflow deploys AWS infrastructure via CDK on `main` branch updates.

---

## **Component Details**

### 1. **`Data_ingestion_stack.py`**  
**Purpose**: Infrastructure setup for data processing.  
**Logic Flow**:  
- Creates S3 buckets (`raw`, `processed`, `quarantined`).  
- Initializes DynamoDB table for tracking metadata.  
- Configures SNS/SQS notifications for pipeline events.  

**Note**: Foundation for future data transformations.

---

### 2. **`lambda_function.py`**  
**Purpose**: Serverless orchestration of data processing.  
**Workflow**:  
1. Checks for new files in S3 by comparing timestamps in DynamoDB.  
2. Triggers SageMaker processing job (scikit-learn container) for valid data.  
3. Routes output to `processed` or `quarantined` buckets.  
4. Updates DynamoDB with latest processing timestamp.  

**Output**: Returns processing job details or "No new files" status.

---

### 3. **`process.py`** (Data Validation Module)  
**Key Functions**:  
- `validate_data()`:  
  - Checks for required columns: `customer_id`, `activity_type`, `timestamp`, `value`.  
  - Enforces data types:  
    - `customer_id` → Integer  
    - `activity_type` → Text  
    - `timestamp` → Datetime  
    - `value` → Decimal  
  - Auto-adds missing columns with defaults.  
  - Logs warnings/errors for unresolved issues.  

**Outcome**: Ensures only validated data progresses downstream.

---

### 4. **GitHub Workflow (`deploy.yml`)**  
**Pipeline Automation**:  
```yaml
name: Deploy Pipeline
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy AWS Infrastructure
        run: |
          pip install -r requirements.txt
          cdk deploy