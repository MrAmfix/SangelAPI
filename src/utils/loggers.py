import logging
import inspect
from functools import wraps


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def api_logs(handler):
    @wraps(handler)
    async def wrapper(*args, **kwargs):
        bound_arguments = inspect.signature(handler).bind(*args, **kwargs).arguments
        params = {key: value for key, value in bound_arguments.items() if key != 'session'}
        log_text = f"Handler: {handler.__name__} | Params: {params}"

        try:
            res = await handler(*args, **kwargs)
        except Exception as e:
            logger.error(f"{log_text} | Exception: {str(e)}")
            raise
        finally:
            logger.info(log_text)
            logger.debug("---------------------------")
        return res

    return wrapper
