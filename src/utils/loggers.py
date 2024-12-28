import logging
import inspect
import colorlog
from functools import wraps


formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)s | %(message)s",
    log_colors={
        "DEBUG": "blue",
        "INFO": "blue",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)
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
            res = await handler(*args, **kwargs)
            logger.info(f"[INFO] | {log_text}")
            return res
        except Exception as e:
            logger.error(f"[ERROR] | {log_text} | Exception: {str(e)}")
            raise
        finally:
            logger.debug("---------------------------")

    return wrapper
