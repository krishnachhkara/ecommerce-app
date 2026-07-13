from pwdlib import PasswordHash
import jwt
from app.core.config import settings
from datetime import datetime,timedelta,timezone
from fastapi import HTTPException,status,Depends
from app.db.database import get_db
from fastapi.security import OAuth2PasswordBearer
<<<<<<< HEAD
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession

password_hasher = PasswordHash.recommended()
=======
from app.models.user import User,UserRole
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.enums import TokenType



#----------------Password Management------------------
password_hasher = PasswordHash.recommended()
refresh_token_hasher = PasswordHash.recommended()
>>>>>>> 4e815fb (feat: implement product and cart modules)

def hash_password(password:str)->str:
    return password_hasher.hash(password)

def verify_password(plain_password:str,hashed_password:str)->bool:
    return password_hasher.verify(plain_password,hashed_password)

<<<<<<< HEAD
=======
#---------------------Jwt Creation-------------------

#create access token helper 
def _create_token(user_id: int,token_type: TokenType,expires_delta: timedelta)->tuple[str,datetime]:
    expire = datetime.now(timezone.utc) + expires_delta

    payload = {
        "sub" : str(user_id),
        "exp": expire,
        "type":token_type
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return token,expire




def create_access_token(user_id:int)->str:

    token,_ = _create_token(
        user_id,
        token_type=TokenType.ACCESS,
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRATION_MINUTES
        )
    )
    return token #here expire time is ignored _

def create_refresh_token(user_id: int) -> tuple[str, datetime]:

    return _create_token(
        user_id=user_id,
        token_type=TokenType.REFRESH,
        expires_delta=timedelta(
            days=settings.REFRESH_TOKEN_EXPIRATION_DAYS
        ),
    )


#------------------Jwt Verification---------------

class InvalidTokenError(Exception):
    pass

#helper function for decoding the jwt token for both access and refresh
def _decode_token(token: str,expected_type: TokenType) -> int:
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])

        subject = payload.get("sub")

        token_type = payload.get("type")

        if token_type != expected_type:
            raise InvalidTokenError()

        if subject is None:
            raise InvalidTokenError()
        
    except (jwt.PyJWTError, ValueError, TypeError):
        raise InvalidTokenError()    
    

    return int(subject)

def decode_access_token(token:str)-> int:
    return _decode_token(
        token,
        TokenType.ACCESS
    )
    
def decode_refresh_token(token: str) -> int:
    return _decode_token(
        token,
        TokenType.REFRESH
    )


#------------------------Authentication Dependencies----------------

oauth_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

async def get_current_user(token: str = Depends(oauth_scheme),db:AsyncSession = Depends(get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        },
    )

    try:
        subject = decode_access_token(token=token)
           
    except InvalidTokenError:
        raise credentials_exception
    
    user = await db.get(User,subject)
    
    if not user:
        raise credentials_exception

    return user    


async def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    return current_user


#--------------------Refresh Token Hashing-----------------


def hash_refresh_token(token:str)->str:
    return refresh_token_hasher.hash(token)

def verify_refresh_token_hash(plain_token:str,hashed_token:str)->bool:
    return refresh_token_hasher.verify(plain_token,hashed_token)

>>>>>>> 4e815fb (feat: implement product and cart modules)

# create_access_token()
#
# Generates a JWT token for an authenticated user.
#
# Input:
# user_id
#
# Steps:
# 1. Calculate expiration time.
# 2. Build JWT payload.
# 3. Add:
#       sub -> user id
#       exp -> expiration time
# 4. Sign token using SECRET_KEY and ALGORITHM.
# 5. Return encoded JWT string.
#
# Output:
# Signed JWT token string
#
# The caller only provides the user identifier.
<<<<<<< HEAD
# JWT configuration is handled internally using settings.

def create_access_token(user_id:int)->str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRATION_MINUTES)
    
    payload  = {"sub":str(user_id),"exp":expire}

    token  = jwt.encode(payload,settings.SECRET_KEY,algorithm=settings.ALGORITHM)

    return token 


class InvalidTokenError(Exception):
    pass


#dict(key:str and value:any type used for datetime and other) dict[str,Any]:
def decode_access_token(token:str)-> str:
    
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])

        subject = payload.get("sub")

        if not subject:
            raise InvalidTokenError()
        
    except jwt.PyJWTError:
        raise InvalidTokenError()    
    

    return subject

oauth_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

async def get_current_user(token: str = Depends(oauth_scheme),db:AsyncSession = Depends(get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        },
    )

    try:
        subject = decode_access_token(token=token)
           
    except InvalidTokenError:
        raise credentials_exception
    
    user = await db.get(User,int(subject))
    
    if not user:
        raise credentials_exception

    return user    

=======
# JWT configuration is handled internally using settings.
>>>>>>> 4e815fb (feat: implement product and cart modules)
