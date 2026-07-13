from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str

    SECRET_KEY : str

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRATION_MINUTES:int = 30
<<<<<<< HEAD
=======
    
    REFRESH_TOKEN_EXPIRATION_DAYS:int = 30

    IMAGEKIT_PUBLIC_KEY: str

    IMAGEKIT_PRIVATE_KEY: str

    IMAGEKIT_URL_ENDPOINT: str
>>>>>>> 4e815fb (feat: implement product and cart modules)

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()    
<<<<<<< HEAD
=======

print(settings.IMAGEKIT_URL_ENDPOINT)
>>>>>>> 4e815fb (feat: implement product and cart modules)
