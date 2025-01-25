import logging
import inspect
from functools import wraps
from colorlog import ColoredFormatter


class CustomColoredFormatter(ColoredFormatter):
    def format(self, record):
        levelname = record.levelname
        if record.levelname == "DEBUG":
            return f"\033[37m{levelname:<8} {record.getMessage()}\033[0m"
        else:
            formatted_message = super().format(record)
            return formatted_message.replace(f"{levelname}:",
                                             f"{levelname:<8}")


handler = logging.StreamHandler()
formatter = CustomColoredFormatter(
    "%(log_color)s%(levelname)s:%(reset)s %(message)s",
    log_colors={
        "DEBUG": "white",
        "INFO": "cyan",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
)
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
            logger.debug('----------------------------')
            logger.info(log_text)
            return await handler(*args, **kwargs)
        except Exception as e:
            logger.error(f"{type(e)}: {str(e)}")
            raise

    return wrapper
