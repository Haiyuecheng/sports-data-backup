# process_videos.py
import json
import boto3
import requests
from io import BytesIO
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get environment variables
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
INPUT_KEY = os.getenv("INPUT_KEY", "highlights/basketball_highlights.json")
OUTPUT_KEY_PREFIX = os.getenv("OUTPUT_KEY_PREFIX", "videos/")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "SportsHighlights")

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb', region_name=AWS_REGION)

def load_video_records_from_s3(bucket_name, key):
    """Load video records from a JSON file in S3."""
    s3 = boto3.client("s3", region_name=AWS_REGION)
    try:
        response = s3.get_object(Bucket=bucket_name, Key=key)
        data = json.loads(response['Body'].read().decode('utf-8'))
        logger.info(f"Loaded video records from S3: {json.dumps(data, indent=2)}")
        return data.get("videos", [])
    except Exception as e:
        logger.error(f"Error retrieving JSON file from S3: {e}")
        return []

def store_highlight_in_dynamodb(video):
    """Store a video highlight record in DynamoDB."""
    try:
        dynamodb.put_item(
            TableName=DYNAMODB_TABLE,
            Item={
                'Id': {'S': video['id']},
                'Title': {'S': video['title']},
                'Url': {'S': video['url']}
            }
        )
        logger.info(f"Stored video highlight in DynamoDB: {video['title']}")
    except Exception as e:
        logger.error(f"Error storing highlight in DynamoDB: {e}")

def process_videos():
    """
    Fetch the highlights JSON file from S3, iterate over all video URLs, download each video,
    and upload them back to S3.
    """
    try:
        video_records = load_video_records_from_s3(S3_BUCKET_NAME, INPUT_KEY)
        if not video_records:
            logger.error("No video records found in the JSON file.")
            return

        for video in video_records:
            logger.info(f"Processing video record: {json.dumps(video, indent=2)}")
            if 'id' not in video:
                logger.error(f"Video record missing 'id': {video}")
                continue
            logger.info(f"Processing video: {video['title']} ({video['url']})")
            # Store the video highlight in DynamoDB
            store_highlight_in_dynamodb(video)
            # Add your video processing logic here

    except Exception as e:
        logger.error(f"Error processing videos: {e}")

if __name__ == "__main__":
    process_videos()
