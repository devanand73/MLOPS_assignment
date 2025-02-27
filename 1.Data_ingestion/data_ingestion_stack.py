# File: data_ingestion_stack.py
from aws_cdk import (
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_events as events,
    aws_events_targets as targets,
    aws_iam as iam,
    aws_sns as sns,
    aws_dynamodb as dynamodb,
    core
)

class DataIngestionStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # S3 Buckets
        raw_bucket = s3.Bucket(self, "CustomerActivityRaw")
        processed_bucket = s3.Bucket(self, "CustomerActivityProcessed", versioned=True)
        quarantine_bucket = s3.Bucket(self, "CustomerActivityQuarantine")

        # DynamoDB Table
        state_table = dynamodb.Table(
            self, "DataIngestionState",
            partition_key=dynamodb.Attribute(name="pipeline_id", type=dynamodb.AttributeType.STRING)
        )

        # SNS Topic
        alert_topic = sns.Topic(self, "AlertTopic")

        # Lambda Role
        lambda_role = iam.Role(self, "LambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")]
        )
        raw_bucket.grant_read(lambda_role)
        state_table.grant_read_write_data(lambda_role)
        lambda_role.add_to_policy(iam.PolicyStatement(
            actions=["sagemaker:CreateProcessingJob"], resources=["*"]
        ))

        # SageMaker Processing Role
        processing_role = iam.Role(self, "ProcessingRole",
            assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com")
        )
        raw_bucket.grant_read(processing_role)
        processed_bucket.grant_write(processing_role)
        quarantine_bucket.grant_write(processing_role)
        alert_topic.grant_publish(processing_role)

        # Lambda Function
        ingestion_lambda = lambda_.Function(self, "IngestionLambda",
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.from_asset("lambda"),
            handler="lambda_function.lambda_handler",
            role=lambda_role,
            environment={
                "STATE_TABLE": state_table.table_name,
                "PROCESSING_ROLE_ARN": processing_role.role_arn,
                "SNS_TOPIC_ARN": alert_topic.topic_arn
            }
        )

        # EventBridge Rule
        events.Rule(self, "HourlyRule",
            schedule=events.Schedule.rate(core.Duration.hours(1)),
            targets=[targets.LambdaFunction(ingestion_lambda)]
        )