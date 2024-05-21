from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class UserCredentials(BaseModel):
    user_email: EmailStr
    password: str


class CreateUser(BaseModel):
    user_email: EmailStr
    user_password: Annotated[str, MinLen(4), MaxLen(16)]
    active: bool = True
    superuser: bool = False


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True, from_attributes=True)

    user_email: EmailStr
    active: bool = False
    superuser: bool = False
