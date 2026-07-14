from app.api.v1.auth import router as auth_router
from fastapi import FastAPI
from app.api.v1.test import router as test_router
from app.api.v1.product import router as product_router

app = FastAPI()

app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

# app.include_router(test_router)
# app.include_router(product_router)

app.include_router(
    product_router,
    prefix="/api/v1/products",
    tags=["Products"]
)