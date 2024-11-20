from typing import Any
import datetime


def image_name_rename()-> str:

    format = datetime.datetime.now().replace(microsecond=0).isoformat("-")
    image_name = "image-" + format

    return image_name





