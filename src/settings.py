import os
from dotenv import load_dotenv


load_dotenv()

UPLOAD_FOLDER = "img"
MAX_FILE_SIZE = 2 * 1024 * 1024
DATABASE_URL = f'postgresql+asyncpg://{os.environ.get("DB_USER")}:{os.environ.get("DB_PASS")}@{os.environ.get("DB_HOST")}:{os.environ.get("DB_PORT")}/{os.environ.get("DB_NAME")}'
