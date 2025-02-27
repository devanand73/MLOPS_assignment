# File: lambda/lambda_function.py
import boto3
import time

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ["STATE_TABLE"])

    # Get last processed timestamp
    response = table.get_item(Key={'pipeline_id': 'customer_activity'})
    last_processed = response.get('Item', {}).get('last_processed_timestamp', 0)

    # List new files
    new_files = []
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket='customer-activity-raw'):
        for obj in page.get('Contents', []):
            if obj['LastModified'].timestamp() > last_processed:
                new_files.append(obj['Key'])

    if not new_files:
        return {"status": "No new files"}

    # Trigger SageMaker Processing Job
    sm_client = boto3.client('sagemaker')
    job_name = f"data-processing-{int(time.time())}"
    sm_client.create_processing_job(
        ProcessingJobName=job_name,
        AppSpecification={
            "ImageUri": "683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-scikit-learn:0.23-1-cpu-py3",
            "ContainerEntrypoint": ["python", "process.py"],
            "ContainerArguments": [
                "--input-s3", "s3://customer-activity-raw",
                "--output-s3", "s3://customer-activity-processed",
                "--quarantine-s3", "s3://customer-activity-quarantine"
            ]
        },
        RoleArn=os.environ["PROCESSING_ROLE_ARN"],
        ProcessingResources={
            "ClusterConfig": {"InstanceCount": 1, "InstanceType": "ml.t3.medium"}
        }
    )

    # Update DynamoDB
    table.put_item(Item={'pipeline_id': 'customer_activity', 'last_processed_timestamp': int(time.time())})

    return {"status": "Job started", "job_name": job_name}