from app.schemas.product import ProductCreate
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product,ProductImage
from app.services.imagekit_service import upload_image



class ProductImageRequiredError(Exception):
    pass

class InvalidPrimaryImageError(Exception):
    pass

class ImageUploadError(Exception):
    pass

async def create_product(
    product_data: ProductCreate,images: list[UploadFile],primary_image_index: int,db: AsyncSession
) -> Product:
    
    if not images:
        raise ProductImageRequiredError()
    
    if (primary_image_index < 0 or primary_image_index >= len(images)):
        raise InvalidPrimaryImageError()
    

    uploaded_urls = []

    try:

        for image in images:
            url = await upload_image(image=image,folder="products")
            uploaded_urls.append(url)

    except Exception as e:
        raise ImageUploadError() from e
    

    try:

        product = Product(
            name = product_data.name,
            description = product_data.description,
            price= product_data.price,
            category= product_data.category,
            subcategory= product_data.subcategory,
            sizes= product_data.sizes,
            bestseller= product_data.bestseller
            )
        
        db.add(product)

        await db.flush()

        for index, url in enumerate(uploaded_urls):

            image = ProductImage(
                product_id=product.id,
                image_url=url,
                is_primary=(index == primary_image_index)
            )

            db.add(image)

        await db.commit()

    except Exception:
        await db.rollback()
        raise
    
    await db.refresh(product)
    print("Service done")
    return product
