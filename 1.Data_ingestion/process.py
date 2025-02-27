# File: process.py
import argparse
import pandas as pd
import os
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

EXPECTED_COLUMNS = {
    "customer_id": "int64",
    "activity_type": "object",
    "timestamp": "datetime64[ns]",
    "value": "float64"
}

def validate_data(df):
    # Check missing columns
    missing = set(EXPECTED_COLUMNS.keys()) - set(df.columns)
    for col in missing:
        df[col] = pd.NA
        logger.warning(f"Added missing column: {col}")

    # Validate data types
    for col, dtype in EXPECTED_COLUMNS.items():
        if col not in df.columns:
            continue
        try:
            if dtype == "datetime64[ns]":
                df[col] = pd.to_datetime(df[col], errors="coerce")
            else:
                df[col] = df[col].astype(dtype)
        except Exception as e:
            logger.error(f"Column {col} validation failed: {e}")
            df[col] = pd.NA  # Auto-correct invalid values

    # Split valid/invalid rows
    valid = df.dropna()
    invalid = df[df.isnull().any(axis=1)]
    return valid, invalid

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-s3", type=str)
    parser.add_argument("--output-s3", type=str)
    parser.add_argument("--quarantine-s3", type=str)
    args = parser.parse_args()

    # Download data from S3
    s3 = boto3.client("s3")
    input_files = []
    for obj in s3.list_objects(Bucket=args.input_s3.split("/")[2])["Contents"]:
        s3.download_file(args.input_s3.split("/")[2], obj["Key"], f"/tmp/{obj['Key']}")
        input_files.append(f"/tmp/{obj['Key']}")

    # Process all files
    for file in input_files:
        df = pd.read_csv(file)
        valid, invalid = validate_data(df)

        # Upload valid data
        valid.to_csv(f"{os.path.basename(file)}", index=False)
        s3.upload_file(
            f"{os.path.basename(file)}",
            args.output_s3.split("/")[2],
            f"processed/{os.path.basename(file)}"
        )

        # Upload invalid data
        if not invalid.empty:
            invalid.to_csv(f"invalid_{os.path.basename(file)}", index=False)
            s3.upload_file(
                f"invalid_{os.path.basename(file)}",
                args.quarantine_s3.split("/")[2],
                f"quarantine/{os.path.basename(file)}"
            )

    # Send alert if anomalies detected
    if not invalid.empty:
        sns = boto3.client("sns")
        sns.publish(
            TopicArn=os.environ["SNS_TOPIC_ARN"],
            Message=f"Anomalies detected in {len(invalid)} rows."
        )