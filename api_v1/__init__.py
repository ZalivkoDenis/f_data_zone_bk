from fastapi import APIRouter

# from .products import products_router
from .auth import auth_router

# from .demo_auth.demo_jwt_auth import router as demo_jwt_auth_router

router = APIRouter()

router.include_router(
    router=auth_router,
    # prefix="/auth",
    # tags=["auth"],
)
