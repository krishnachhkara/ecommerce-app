from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie

from app.db.database import get_db
from app.schemas.auth import UserLogin,UserRegister,TokenResponse,UserResponse
from app.services.auth_service import register_user,login_user,UserAlreadyExistsError,InvalidCredentialsError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_current_user
from app.models.user import User
from app.services.auth_service import refresh_access_token, InvalidTokenError, logout_user
from app.core.exceptions import credentials_exception

router = APIRouter()


@router.get('/me')
async def test(current_user:User = Depends(get_current_user)):
    return "Success"

@router.post('/register',response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def register(payload:UserRegister,db:AsyncSession = Depends(get_db)):
    try:
        user = await register_user(payload,db)
        return user

    except UserAlreadyExistsError:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Email already registered"
    )


@router.post('/login', response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    payload: UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    try:
        access_token, refresh_token = await login_user(payload, db)

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=30 * 24 * 60 * 60,
        )

    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )
@router.post('/refresh',response_model=TokenResponse,status_code=status.HTTP_200_OK)
async def refresh(
    refresh_token:str|None = Cookie(default=None),
    db:AsyncSession= Depends(get_db),
    )->TokenResponse:

    if refresh_token is None:
        raise credentials_exception
    
    try:
    
        return await refresh_access_token(refresh_token,db)
    
    except InvalidTokenError:
        raise credentials_exception
    

@router.post('/logout',status_code=status.HTTP_200_OK)
async def logout(
    response:Response,
    refresh_token:str|None = Cookie(default=None),
    db:AsyncSession= Depends(get_db)
    ):
    
    if refresh_token is None:
        raise credentials_exception
    
    try:
        await logout_user(refresh_token,db)

    except InvalidTokenError:
        raise credentials_exception
    
    
    response.delete_cookie(key="refresh_token")

    return {
    "message": "Logged out successfully"
    }    

