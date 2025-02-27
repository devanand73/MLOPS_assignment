aws s3api create-bucket --bucket customer-activity-raw
aws s3api create-bucket --bucket customer-activity-processed
aws s3api create-bucket --bucket customer-activity-quarantine
aws s3api put-bucket-versioning --bucket customer-activity-processed --versioning-configuration Status=Enabled