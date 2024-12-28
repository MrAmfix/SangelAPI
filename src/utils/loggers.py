import logging
import inspect
from functools import wraps

from starlette.status import HTTP_400_BAD_REQUEST

from src.utils.moscow_datetime import datetime_now_moscow
from fastapi import Request


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def api_logs(handler):
    @wraps(handler)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get('request', None) or next((arg for arg in args if isinstance(arg, Request)), None)
        path = request.url.path if request else "Unknown Path"

        bound_arguments = inspect.signature(handler).bind(*args, **kwargs).arguments
        params = {key: value for key, value in bound_arguments.items() if key != 'session'}

        logger.info(f"[{datetime_now_moscow()}] | API [{path}] | Params: {params} | Handler: {handler.__name__}")
        try:
            return await handler(*args, **kwargs)
        except Exception as e:
            logger.error(f"[{datetime_now_moscow()}] | API [{path}] | Params: {params} | {e}")
            raise

    return wrapper
