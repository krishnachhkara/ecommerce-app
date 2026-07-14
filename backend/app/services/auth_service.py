from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import UserRegister,UserLogin,TokenResponse
from app.models.user import User

from app.models.refresh_token import RefreshToken
from sqlalchemy import select
from app.core.security import (hash_password,verify_password,create_access_token,create_refresh_token
,hash_refresh_token,decode_refresh_token,verify_refresh_token_hash,InvalidTokenError)



class UserAlreadyExistsError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass


async def register_user(user_data: UserRegister,db: AsyncSession) -> User:
    stmt = select(User).where(User.email == user_data.email)
    check = await db.execute(stmt)
    result =  check.scalar_one_or_none()

    if result:
        raise UserAlreadyExistsError()
    
    user = User(
        name = user_data.name,
        email = user_data.email,
        hashed_password = hash_password(user_data.password)
    )

    
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def login_user( user_data: UserLogin, db: AsyncSession)->tuple[str, str]:
   
    stmt = select(User).where(User.email == user_data.email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise InvalidCredentialsError()
    
    verification = verify_password(user_data.password,user.hashed_password)

    if not verification:
        raise InvalidCredentialsError()
    
    access_token = create_access_token(user.id)
    refresh_token,expires_at = create_refresh_token(user.id)
    hashed_refresh_token = hash_refresh_token(refresh_token)

    stored_tokens = RefreshToken(
        user_id = user.id,
        hashed_token = hashed_refresh_token,
        expires_at = expires_at
    )
    db.add(stored_tokens)
    await db.commit()

    return access_token,refresh_token


#-------------creating helper function for logout and refresh------------------

async def _find_matching_refresh_token(refresh_token:str,db:AsyncSession)->RefreshToken:
    user_id = decode_refresh_token(refresh_token)
    stmt = select(RefreshToken).where(RefreshToken.user_id==user_id)
    result = await db.execute(stmt)
    stored_tokens = result.scalars().all()

    matching_token = None

    for stored_token in stored_tokens:
        if verify_refresh_token_hash(refresh_token,stored_token.hashed_token):
            matching_token = stored_token
            break

    if matching_token is None:
        raise InvalidTokenError()
    
    return matching_token
    
async def logout_user(refresh_token: str,db:AsyncSession)->None:
    matching_token = await _find_matching_refresh_token(refresh_token,db)
    
    await db.delete(matching_token)
    await db.commit()




async def refresh_access_token(
    refresh_token: str,
    db: AsyncSession,
) -> TokenResponse:
    matching_token = await _find_matching_refresh_token(refresh_token,db)
    
    token = create_access_token(matching_token.user_id)

    return TokenResponse(
    access_token=token,
    token_type="bearer",
    )
