# config.py
import os
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

###################################
# RapidAPI & Fetch-Related Config
###################################
logger.info("Loading RapidAPI & Fetch-Related Config")
API_URL = os.getenv("API_URL", "https://sport-highlights-api.p.rapidapi.com/basketball/highlights")
logger.info(f"API_URL: {API_URL}")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "sport-highlights-api.p.rapidapi.com")
logger.info(f"RAPIDAPI_HOST: {RAPIDAPI_HOST}")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")  # No default, must be set at runtime
logger.info(f"RAPIDAPI_KEY: {RAPIDAPI_KEY}")

# Use the current day in YYYY-MM-DD format as the default date
DATE = os.getenv("DATE", datetime.utcnow().strftime("%Y-%m-%d"))
logger.info(f"DATE: {DATE}")
LEAGUE_NAME = os.getenv("LEAGUE_NAME", "NCAA")
logger.info(f"LEAGUE_NAME: {LEAGUE_NAME}")
LIMIT = int(os.getenv("LIMIT", "10"))
logger.info(f"LIMIT: {LIMIT}")

###################################
# AWS & S3
###################################
logger.info("Loading AWS & S3 Config")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
logger.info(f"S3_BUCKET_NAME: {S3_BUCKET_NAME}")
AWS_REGION = os.getenv("AWS_REGION")
logger.info(f"AWS_REGION: {AWS_REGION}")

###################################
# DynamoDB
###################################
logger.info("Loading DynamoDB Config")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "SportsHighlights")
logger.info(f"DYNAMODB_TABLE: {DYNAMODB_TABLE}")

###################################
# MediaConvert
###################################
logger.info("Loading MediaConvert Config")
MEDIACONVERT_ENDPOINT = os.getenv("MEDIACONVERT_ENDPOINT")
logger.info(f"MEDIACONVERT_ENDPOINT: {MEDIACONVERT_ENDPOINT}")
MEDIACONVERT_ROLE_ARN = os.getenv("MEDIACONVERT_ROLE_ARN")
logger.info(f"MEDIACONVERT_ROLE_ARN: {MEDIACONVERT_ROLE_ARN}")

###################################
# Video Paths in S3
###################################
logger.info("Loading Video Paths in S3 Config")
INPUT_KEY = os.getenv("INPUT_KEY", "highlights/basketball_highlights.json")
logger.info(f"INPUT_KEY: {INPUT_KEY}")
# Note: For multiple videos, you may want to use a key pattern rather than a fixed name.
OUTPUT_KEY_PREFIX = os.getenv("OUTPUT_KEY_PREFIX", "videos/")
logger.info(f"OUTPUT_KEY_PREFIX: {OUTPUT_KEY_PREFIX}")

###################################
# run_all.py Retry/Delay Config
###################################
logger.info("Loading run_all.py Retry/Delay Config")
RETRY_COUNT = int(os.getenv("RETRY_COUNT", "3"))
logger.info(f"RETRY_COUNT: {RETRY_COUNT}")
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "30"))
logger.info(f"RETRY_DELAY: {RETRY_DELAY}")
WAIT_TIME_BETWEEN_SCRIPTS = int(os.getenv("WAIT_TIME_BETWEEN_SCRIPTS", "60"))
logger.info(f"WAIT_TIME_BETWEEN_SCRIPTS: {WAIT_TIME_BETWEEN_SCRIPTS}")
