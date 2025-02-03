from typing import Optional
from pydantic import UUID4
from uuid import UUID


def image_name_rename(user_id: UUID) -> str:
        result = f"user_photo_{user_id}"
        return result

