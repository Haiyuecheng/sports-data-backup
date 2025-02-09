# run_all.py
import subprocess
import time
import boto3
import logging
from botocore.exceptions import ClientError

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
import os
from dotenv import load_dotenv
load_dotenv()

# Get environment variables
AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-2")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# Initialize S3 client
s3_client = boto3.client('s3', region_name=AWS_REGION)

from config import (
    RETRY_COUNT,
    RETRY_DELAY,
    WAIT_TIME_BETWEEN_SCRIPTS
)

def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region"""
    try:
        if region is None:
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        logger.info(f"Bucket {bucket_name} created successfully.")
    except ClientError as e:
        logger.error(f"Error creating bucket: {e}")
        return False
    return True

def run_script(script_name, retries=RETRY_COUNT, delay=RETRY_DELAY):
    """
    Run a script with retry logic and a delay.
    """
    attempt = 0
    while attempt < retries:
        try:
            print(f"Running {script_name} (attempt {attempt + 1}/{retries})...")
            subprocess.run(["python", script_name], check=True)
            print(f"{script_name} completed successfully.")
            return
        except subprocess.CalledProcessError as e:
            print(f"Error running {script_name}: {e}")
            attempt += 1
            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"{script_name} failed after {retries} attempts.")
                raise e

def main():
    try:
        # Create the S3 bucket
        if not create_bucket(S3_BUCKET_NAME, AWS_REGION):
            logger.error("Bucket creation failed.")
        else:
            logger.info("Bucket created successfully.")

        # Step 1: Run fetch.py (fetch data, save to S3, and store in DynamoDB)
        run_script("fetch.py")

        print("Waiting for resources to stabilize...")
        time.sleep(WAIT_TIME_BETWEEN_SCRIPTS)

        # Step 2: Run process_videos.py (now processing all video URLs)
        run_script("process_videos.py")

        print("Waiting for resources to stabilize...")
        time.sleep(WAIT_TIME_BETWEEN_SCRIPTS)

        # Step 3: Run mediaconvert_process.py (if needed)
        run_script("mediaconvert_process.py")

        print("All scripts executed successfully.")
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    main()
