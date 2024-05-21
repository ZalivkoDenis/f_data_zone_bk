from datetime import timedelta

from jwt.exceptions import InvalidTokenError

from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status,
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, dependencies as dpd
from .dependencies import (
    http_bearer,
    # get_auth_user_from_token_of_type,
    # UserGetterFromToken,
    get_current_auth_user_for_refresh,
    # oauth2_scheme,
)
from .schemas import TokenInfo, UserSchema, UserCredentials, CreateUser
from .utils import create_access_token, create_refresh_token, TOKEN_TYPE_REFRESH

from core.helpers import db_helper
from core.models import User


router = APIRouter(
    prefix="/auth",
    tags=["Auth JWT"],
    # dependencies=[Depends(http_bearer), Depends(dpd.check_auth_user_to_rights)],
    dependencies=[Depends(http_bearer)],
)


@router.post("/login", response_model=TokenInfo)
async def auth_user_issue_jwt(
    credentials: UserCredentials = Depends(dpd.validate_auth_user),
):
    access_token = create_access_token(UserSchema(user_email=credentials.user_email))
    refresh_token = create_refresh_token(UserSchema(user_email=credentials.user_email))
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post(
    "/refresh",
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
async def auth_refresh_jwt(
    user: User = Depends(get_current_auth_user_for_refresh),
):
    access_token = create_access_token(UserSchema(user_email=user.user_email))
    return TokenInfo(
        access_token=access_token,
    )


@router.patch("/login")
async def change_user_password():
    pass


@router.get("/users/me")
async def read_users_me(
    user: User = Depends(dpd.get_current_active_auth_user),
) -> UserSchema | None:
    res = UserSchema.model_validate(user)
    return res


@router.post("/register", dependencies=[Depends(dpd.user_is_superuser)])
async def register_user(
    user: CreateUser,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> UserSchema:
    user = await crud.create_user(user=user, session=session)
    return UserSchema.model_validate(user)


@router.delete("/deactivate", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_user(
    user: User = Depends(dpd.get_current_active_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.deactivate_user(user=user, session=session)


@router.post("/create_default_admin")
async def create_admin(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_admin_if_not_exists(session=session)
