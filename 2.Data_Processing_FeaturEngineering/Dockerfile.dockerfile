# File: Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Install test dependencies
RUN pip install pytest

# Environment variables
ENV AWS_ACCESS_KEY_ID=
ENV AWS_SECRET_ACCESS_KEY=
ENV MLFLOW_TRACKING_URI=

ENTRYPOINT ["python", "feature_pipeline.py"]
CMD ["--local-run"]

# For tests
ENTRYPOINT ["pytest"]  # Override with docker run ... pytest tests/