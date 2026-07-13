from fastapi import APIRouter, Depends,HTTPException,status
from app.db.database import get_db
from app.schemas.auth import UserLogin,UserRegister,TokenResponse,UserResponse
from app.services.auth_service import register_user,login_user,UserAlreadyExistsError,InvalidCredentialsError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_current_user
from app.models.user import User
from fastapi import UploadFile
from app.services.imagekit_service import upload_image


router = APIRouter()



@router.post("/test-upload")
async def test_upload(
    image: UploadFile
):
    url = await upload_image(
        image=image,
        folder="products"
    )

    return {
        "image_url": url
    }