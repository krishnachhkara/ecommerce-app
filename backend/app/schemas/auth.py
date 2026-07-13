from pydantic import BaseModel,EmailStr,ConfigDict


class UserRegister(BaseModel):
    name: str
    email : EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password:str

class TokenResponse(BaseModel):
    access_token: str
    token_type : str

class UserResponse(BaseModel):
    id: int
    role: str
    name: str
    email:EmailStr   


    model_config = ConfigDict(
    from_attributes=True
)         