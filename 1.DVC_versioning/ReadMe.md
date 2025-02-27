# Data Versioning Protocol

1. **New Data Version**:
   ```bash
   dvc repro  # Process data
   dvc commit  # Record changes
   dvc push  # Store in S3
   git commit -am "Update data version"

   Training with Versioned Data:
   dvc pull  # Get latest data
   dvc checkout data/processed.dvc --rev <commit_hash>

   Audit Trail:
   dvc list --rev HEAD~3..HEAD data/processed.dvc

   ### **9. Best Practices**

1. **Tag Major Versions**:
   ```bash
   dvc tag create v1.0 -d data/processed.dvc
   git push origin --tags

   Automated Versioning Policy:
   # .dvc/config
   cache:
   type: symlink
   shared: group

   Data Version Schema:
   # data_versions.csv
   timestamp,commit_hash,data_path,description
   2023-07-15,a1b2c3d,data/processed,Initial processed dataset

   Security Considerations:
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

This implementation provides:

Full reproducibility of data states
Granular version control for datasets
Integration with existing AWS infrastructure
Automated lineage tracking
Drift detection capabilities
Secure access controls
Key differentiators from previous solution:

Uses DVC's data pipeline capabilities instead of raw S3 versioning
Enables dataset-level versioning rather than file-level
Provides better reproducibility through DVC's dependency tracking
Integrates directly with ML experiment tracking
Offers more granular rollback capabilities
To maintain consistency with previous ingestion pipeline:

Keep raw data in S3 (versioned through AWS)
Use DVC only for processed/curated datasets
Maintain cross-references between S3 raw versions and DVC processed versions