from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr


class EmailSvcBaseInfo(BaseModel):
    user_email: EmailStr
    user_password: Annotated[str, MinLen(4), MaxLen(16)]
    impap_server: str
