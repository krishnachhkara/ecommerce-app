from fastapi import APIRouter,Depends,HTTPException,status,UploadFile,File,Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.product import ProductCreate,ProductCreateResponse
from app.core.security import get_current_admin
from app.db.database import get_db
from app.models.user import User
from app.services.product_service import create_product,ImageUploadError,InvalidPrimaryImageError,ProductImageRequiredError
from decimal import Decimal

router = APIRouter()


@router.post('/',response_model=ProductCreateResponse,status_code=status.HTTP_201_CREATED)
async def create_product_route(
    name:str = Form(...),
    description:str = Form(...),
    price:Decimal = Form(...),
    category:str = Form(...),
    subcategory:str = Form(...),
    bestseller:bool = Form(False),
    primary_image_index:int = Form(...),#(...) means this field is required
    sizes: list[str] = Form(...),

    images: list[UploadFile] = File(...),

    db: AsyncSession = Depends(get_db),

    admin: User = Depends(get_current_admin),
):  
    
    #creating the product object model/ database table content mapping
    product_data = ProductCreate(
    name=name,
    description=description,
    price=price,
    category=category,
    subcategory=subcategory,
    sizes=sizes,
    bestseller=bestseller,
    )
    
    try:
        #calling service
        product = await create_product(
        product_data=product_data,
        images=images,
        primary_image_index=primary_image_index,
        db=db,
        )

    except ProductImageRequiredError:
        raise HTTPException(
            status_code=400,
            detail="At least one product image is required"
        )

    except InvalidPrimaryImageError:
        raise HTTPException(
            status_code=400,
            detail="Invalid primary image index"
        )

    except ImageUploadError:
        raise HTTPException(
            status_code=500,
            detail="Failed to upload images"
        )  

    return ProductCreateResponse(
         id=product.id,
    )