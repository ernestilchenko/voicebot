import os

from dotenv import load_dotenv

load_dotenv()

TOKEN_TELEGRAM = os.getenv('TOKEN_TELEGRAM')
DB_URL = os.getenv('DB_URL')
