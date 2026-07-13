from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.cart import CartItemCreate,CartItemUpdate,CartResponse
from app.core.security import get_user
from app.db.database import get_db
from app.models.user import User
from app.services import cart_service
from app.services.cart_service import ItemNotFoundError,ProductNotFound

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)

@router.post('/items',response_model=CartResponse,status_code=status.HTTP_201_CREATED)
async def add_to_cart(payload:CartItemCreate,db:AsyncSession = Depends(get_db),user:User = Depends(get_user))->CartResponse:
    try:
        response = await cart_service.add_to_cart(user.id,payload,db)
    except ProductNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product Not Found")
    
    return response
    

@router.get('',response_model=CartResponse,status_code=status.HTTP_200_OK)
async def get_cart(db:AsyncSession=Depends(get_db),user:User=Depends(get_user))->CartResponse:
    return await cart_service.get_cart(user.id,db)

@router.patch('/items/{item_id}',status_code=status.HTTP_200_OK)
async def update_cart_item(item_id:int,payload:CartItemUpdate,db:AsyncSession=Depends(get_db),user:User=Depends(get_user))->CartResponse:
    try:
        response = await cart_service.update_cart_item(user.id,item_id,db,payload)

    except ItemNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Cart Item Not Found")
    
    return response

@router.delete('/items/{item_id}',status_code=status.HTTP_204_NO_CONTENT)
async def remove_cart_item(item_id:int,db:AsyncSession=Depends(get_db),user:User=Depends(get_user))->None:
    try:
        await  cart_service.remove_cart_item(user.id,item_id,db)
    except ItemNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Cart Item Not Found")
    
    
    

@router.delete('',status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(db:AsyncSession=Depends(get_db),user:User=Depends(get_user))->None:
    try:
         await cart_service.clear_cart(user.id,db)
    except ItemNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Cart Item Not Found")
    