from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[int]):
    id: int
    first_name: str
    second_name: str
    login: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

class UserCreate(schemas.BaseUserCreate):
    first_name: str
    second_name: str
    login: str
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


# class UserUpdate(schemas.BaseUserUpdate):
#     pass
