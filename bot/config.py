import os

from dotenv import load_dotenv

load_dotenv()

TOKEN_TELEGRAM = os.getenv('TOKEN_TELEGRAM')
DB_URL = os.getenv('DB_URL')

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')
GCS_CREDENTIALS_PATH = os.getenv('GCS_CREDENTIALS_PATH')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')