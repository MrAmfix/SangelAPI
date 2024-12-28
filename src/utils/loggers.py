import logging
import inspect
from functools import wraps
import asyncio


handler = logging.StreamHandler()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def api_logs(handler):
    @wraps(handler)
    async def wrapper(*args, **kwargs):
        bound_arguments = inspect.signature(handler).bind(*args, **kwargs).arguments
        params = {key: value for key, value in bound_arguments.items() if key != 'session'}
        log_text = f"Handler: {handler.__name__} | Params: {params}"

        try:
            logger.info(log_text)
            await asyncio.sleep(0.01)
            res = await handler(*args, **kwargs)
            return res
        except Exception as e:
            logger.error(f"{log_text} | Exception: {str(e)}")
            raise
        finally:
            print("---------------------------")
            await asyncio.sleep(0.01)

    return wrapper
