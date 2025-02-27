# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy dependencies and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code into the container
COPY . .

# Expose the application port
EXPOSE 8000

# Command to run the application using gunicorn with multiple workers for robustness
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "app:app"]