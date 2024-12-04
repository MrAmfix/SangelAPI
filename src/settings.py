import os
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = f'postgresql+asyncpg://{os.environ.get("DB_USER")}:{os.environ.get("DB_PASS")}@{os.environ.get("DB_HOST")}:{os.environ.get("DB_PORT")}/{os.environ.get("DB_NAME")}'

SMS_API_URL = os.environ.get("SMS_API_URL")
SMS_API_KEY = os.environ.get("SMS_API_KEY")
SMS_API_NUMBER = os.environ.get("SMS_API_NUMBER")