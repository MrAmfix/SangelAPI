import logging
import inspect
from functools import wraps
from src.utils.moscow_datetime import datetime_now_moscow
from fastapi import Request


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def api_logs(handler):
    @wraps(handler)
    async def wrapper(*args, **kwargs):
        request: Request = next((arg for arg in args if isinstance(arg, Request)), None)
        path = request.url.path if request else "Unknown Path"

        params = inspect.signature(handler).bind(*args, **kwargs).arguments

        logger.info(f"[{datetime_now_moscow()}] | API [{path}] | Params: {params} | Handler: {handler.__name__}")
        try:
            return await handler(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in API [{path}]: {e}")
            raise

    return wrapper
