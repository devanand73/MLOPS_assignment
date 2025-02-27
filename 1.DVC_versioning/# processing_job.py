# processing_job.py
import os
import subprocess

def main():
    # Pull specific data version
    subprocess.run(["dvc", "pull", "data/processed.dvc", "-r", "s3-storage"])

    # Training code here
    # ...

if __name__ == "__main__":
    main()