import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = f'postgresql+asyncpg://{os.environ.get("DB_USER")}:{os.environ.get("DB_PASS")}@{os.environ.get("DB_HOST")}:{os.environ.get("DB_PORT")}/{os.environ.get("DB_NAME")}'

JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
JWT_REFRESH_TOKEN_EXPIRE_MINUTES = os.environ.get("JWT_REFRESH_TOKEN_EXPIRE_MINUTES")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
