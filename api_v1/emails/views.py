from fastapi import Depends, APIRouter
from starlette import status

from api_v1.auth.dependencies import http_bearer

router = APIRouter(
    prefix="/eserv",
    tags=["Email Servers"],
    dependencies=[Depends(http_bearer)],
)


# Add account
@router.post("/")
async def set_new_account():
    pass


# Get account
@router.get("/{eserv_id}")
async def get_account():
    pass


# Edit account
@router.patch("/{eserv_id}")
async def edit_account():
    pass


# Delete account
@router.delete("/{eserv_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account():
    pass


# Email Servers List


# Get email list by criteria
