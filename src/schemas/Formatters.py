from pydantic import BaseModel, Field, field_validator
import re


class PhoneRequest(BaseModel):
    phone: str = Field(..., description="Phone number")

    @field_validator("phone", mode="before")
    def normalize_phone(self, v):
        return re.sub(r"^8(\d{10})$", r"+7\1", v)
