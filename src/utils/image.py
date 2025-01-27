from typing import Optional
from pydantic import UUID4


def image_name_rename(user_id: str, rewrite: bool, img_name: Optional[str]) -> str:
    try:

        if img_name is None:
            index = 0
            result = f"user_photo_{user_id}_{index}"
            return result

        if rewrite is False:
            last_underscore_index = img_name.rfind("_")
            number_part = img_name[last_underscore_index + 1 :]
            if number_part.isdigit():
                number = int(number_part)
                incremented_number = number + 1
                result = img_name[: last_underscore_index + 1] + str(incremented_number)
                return result
        return None

    except Exception as e:
        raise e