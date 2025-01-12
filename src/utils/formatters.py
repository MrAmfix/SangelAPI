import re
from fastapi import Body


def normalize_phone(phone: str = Body(..., embed=True)):
    return re.sub(r"^8(\d{10})$", r"+7\1", phone)
