import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from src.routers.auth import auth
from src.routers.debug import debug
from src.routers.media import media
from src.routers.settings import settings
from src.routers.events import events
from fastapi import FastAPI


app = FastAPI()


origins = [
    'http://localhost',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin", "Authorization"],
)


# Подключаем все роутеры к App
app.include_router(auth)
app.include_router(debug)
app.include_router(media)
app.include_router(settings)
app.include_router(events)


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
