from datetime import timedelta

from jwt.exceptions import InvalidTokenError

from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status,
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth import crud
from api_v1.auth import dependencies as dpd
from api_v1.auth.schemas import TokenInfo, UserSchema, UserCredentials
from core.helpers import db_helper
from core.cipher import auth_utils
from core.models import User

http_bearer = HTTPBearer()

router = APIRouter(prefix="/auth", tags=["Auth JWT"])


@router.post("/login", response_model=TokenInfo)
async def auth_user_issue_jwt(
    credentials: UserCredentials = Depends(dpd.validate_auth_user),
):
    jwt_payload = {
        # subject
        "sub": credentials.user_email,
        "username": credentials.user_email,
    }
    token = auth_utils.encode_jwt(jwt_payload, expire_timedelta=timedelta(days=30))
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


@router.post("/create_default_admin")
async def create_admin(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_admin_if_not_exists(session=session)
