import logging
import inspect
import colorlog
from functools import wraps


formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)s%(reset)s | %(message)s",
    log_colors={
        "DEBUG": "blue",
        "INFO": "green",
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
            return res
        except Exception as e:
            logger.error(f"{log_text} | Exception: {str(e)}")
            raise
        finally:
            logger.info(log_text)
            logger.debug("---------------------------")

    return wrapper
