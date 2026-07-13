from fastapi import UploadFile
from imagekitio import ImageKit
from app.core.config import settings
import uuid

imagekit = ImageKit(
    private_key=settings.IMAGEKIT_PRIVATE_KEY
)

async def upload_image(
    image: UploadFile,
    folder: str
    ) -> str:

    content = await image.read()#converting image into bytes(req by imagekit)

    filename = f"{uuid.uuid4()}-{image.filename}"

    response = imagekit.files.upload(
        file=content,
        file_name=filename,
        folder=f"/{folder}"
    )

    return response.url