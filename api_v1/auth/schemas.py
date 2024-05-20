from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


class UserCredentials(BaseModel):
    user_email: EmailStr
    password: str


class CreateUser(BaseModel):
    user_email: EmailStr
    user_password: Annotated[str, MinLen(4), MaxLen(16)]


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    user_email: EmailStr
    password: bytes
    active: bool = False
    superuser: bool = False
    #
    # class Config:
    #     orm_mode = True
