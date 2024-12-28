import logging
import inspect
from functools import wraps


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

        uvicorn_logger = logging.getLogger("uvicorn.access")
        uvicorn_logger.propagate = False
        error_occurred = False

        try:
            res = await handler(*args, **kwargs)
            return res
        except Exception as e:
            error_occurred = True
            logger.error(f"{log_text} | Exception: {str(e)}")
            raise
        finally:
            if not error_occurred:
                logger.info(log_text)
            print("---------------------------")

    return wrapper
