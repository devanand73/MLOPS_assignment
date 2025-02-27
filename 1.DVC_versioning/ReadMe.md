# Data Versioning Protocol Documentation

---

## **Core Components**

### 1. **`processing_job.py`**  
**Purpose**: Manage data versioning via DVC for consistent data access.  
**Key Features**:  
- Executes `dvc pull` to retrieve specific versions of `data/processed.dvc` from S3.  
- Synchronizes data files for training workflows.  

**Implementation**:
subprocess.run(["dvc", "pull", "data/processed.dvc", "--remote", "s3-storage"])

2. data_validation.py
Function: get_data_lineage()

Inputs: None
Outputs: Data lineage metadata (versions, tags, history)
Workflow:
Creates DVC repository object.
Uses dvc ls to inspect data/processed.dvc.
Tracks file state, location, and tags across commits.

3. ml_metadata_tracking.py
Integration: Combines DVC + MLflow for experiment tracking.
Process:
data_url = dvc.api.get_url("data/processed.dvc")
with mlflow.start_run():
    mlflow.log_param("data_version", data_url)
    mlflow.log_artifact("data/processed.dvc")

4. monitor_drift.py
Functionality: Detect dataset drift using Kolmogorov-Smirnov test.
Methodology:

Compares current vs. previous dataset versions (Parquet format).
Flags columns with p-value < 0.05 as drifted.

5. CI/CD Pipeline (pipeline.yml)
Automated Workflow:
name: MLOps Pipeline
on: [push]
jobs:
  versioning:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup DVC
        run: pip install dvc[s3]
      - name: Reproduce Pipeline
        run: dvc repro

Data Versioning Protocol

1. **New Data Version**:
   ```bash
   dvc repro  # Process data
   dvc commit  # Record changes
   dvc push  # Store in S3
   git commit -am "Update data version"

2.  **Training with Versioned Data**:
   dvc pull  # Get latest data
   dvc checkout data/processed.dvc --rev <commit_hash>

3.  **Audit Trail**:
   dvc list --rev HEAD~3..HEAD data/processed.dvc

   ### **9. Best Practices**

1. **Tag Major Versions**:
   ```bash
   dvc tag create v1.0 -d data/processed.dvc
   git push origin --tags

2.  **Automated Versioning Policy**:
   # .dvc/config
   cache:
   type: symlink
   shared: group

3.  **Data Version Schema**:
   # data_versions.csv
   timestamp,commit_hash,data_path,description
   2023-07-15,a1b2c3d,data/processed,Initial processed dataset

4.  **Security Considerations:
   # S3 Bucket Policy for DVC
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::mlops-data-versioning",
                "arn:aws:s3:::mlops-data-versioning/*"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:SourceVpc": "vpc-123456"
                }
            }
        }
    ]
}

Key Differentiators
✅ Reproducibility: Full data state recreation via DVC pipelines
✅ Granular Control: Dataset-level versioning (vs. file-level in S3)
✅ ML Integration: Direct links between data versions and MLflow experiments
✅ Rollbacks: dvc checkout <commit_hash> for dataset restoration

**Consistency with Previous Pipeline**
Raw Data: Versioned via AWS S3
Processed Data: Versioned via DVC
Cross-References: Maintain mapping between S3 raw versions and DVC processed versions