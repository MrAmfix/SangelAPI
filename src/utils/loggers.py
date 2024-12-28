import inspect
import logging
import colorlog
from functools import wraps


handler = colorlog.StreamHandler()
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
handler.setFormatter(formatter)
logger = logging.getLogger("decorator_logger")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def api_logs(handler_func):
    @wraps(handler_func)
    async def wrapper(*args, **kwargs):
        # Получение аргументов функции
        bound_arguments = inspect.signature(handler_func).bind(*args, **kwargs).arguments
        params = {key: value for key, value in bound_arguments.items() if key != 'session'}
        log_text = f"Handler: {handler_func.__name__} | Params: {params}"

        try:
            result = await handler_func(*args, **kwargs)
            logger.info(log_text)
            logger.debug("----------------------")
            return result
        except Exception as e:
            logger.error(f"{log_text} | Exception: {str(e)}")
            logger.debug("----------------------")
            raise

    return wrapper
