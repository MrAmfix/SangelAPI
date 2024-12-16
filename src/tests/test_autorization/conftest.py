from typing import Optional
from src.schemas import UserModels
import pytest
from src.utils.enums import DefaultVisibilityType
from pydantic import UUID4, BaseModel, ConfigDict


class TestUserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    surname: str
    patronymic: Optional[str] = None
    phone: str
    email: Optional[str] = None


@pytest.fixture(scope="function")
def create_test_user():
    test_user = TestUserModel(
        name="Иван",
        surname="Иванов",
        patronymic="Иванович",
        phone="+71234567890",
        email="test@test.by",
    )
    return test_user.model_dump()
