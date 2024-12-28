import logging
import inspect
from functools import wraps
from colorlog import ColoredFormatter


class CustomColoredFormatter(ColoredFormatter):
    def format(self, record):
        if record.levelname == "DEBUG":
            self.log_colors["DEBUG"] = "white"
            return f"{self.log_colors['DEBUG']}DEBUG:{self.reset} {record.getMessage()}"
        else:
            return super().format(record)


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
        log_text = f"     Handler: {handler.__name__} | Params: {params}"

        try:
            logger.debug('----------------------------')
            logger.info(log_text)
            return await handler(*args, **kwargs)
        except Exception as e:
            logger.error(f"     Exception: {str(e)}")
            raise

    return wrapper
