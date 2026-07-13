from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.cart import CartItemCreate,CartItemUpdate,CartResponse,CartItemResponse
from sqlalchemy import select
from app.models.cart import Cart,CartItem
from sqlalchemy.orm import joinedload
from app.models.product import Product
from decimal import Decimal

class CartNotFoundError(Exception):
    pass

class ItemNotFoundError(Exception):
    pass

class ProductNotFound(Exception):
    pass

#----------------------Helper Functions ---------------------------
async def _get_or_create_cart(
    user_id: int,
    db: AsyncSession,
) -> Cart:

    stmt = select(Cart).where(Cart.user_id == user_id)

    cart = await db.scalar(stmt)

    if not cart:
        cart = Cart(user_id=user_id)

        db.add(cart)

        await db.flush()

    return cart

async def _build_cart_response(cart:Cart,db:AsyncSession)->CartResponse:
    
    items:list[CartItemResponse] = []

    stmt = select(CartItem).where(CartItem.cart_id==cart.id).options(
        joinedload(CartItem.product).selectinload(Product.images) 
    )
    cart_items = await db.scalars(stmt)
    
    total = Decimal("0") 

    for item in cart_items:

        item_total = item.product.price * item.quantity

        total += item_total  
         
        primary_image_url = ""
        for product_image in item.product.images:
           if product_image.is_primary:
            primary_image_url = product_image.image_url
            break
            
        items.append( CartItemResponse(
            product_id= item.product_id,
            name=item.product.name,
            price=item.product.price,
            quantity=item.quantity,
            image_url=primary_image_url
            )
        )
        

    return CartResponse(
        items=items,
        total=total
    )


    

async def add_to_cart(
    user_id: int,
    payload: CartItemCreate,
    db: AsyncSession,
) -> CartResponse:

# This function will bring together everything we've built:

# ✅ Verify the product exists.
# ✅ Get or create the user's cart.
# ✅ Check if the product is already in the cart.
# ✅ If yes, increase the quantity.
# ✅ If no, create a new CartItem.
# ✅ Commit the transaction.
# ✅ Return the updated cart.

    stmt = select(Product).where(Product.id== payload.product_id)
    product = await db.scalar(stmt)
    if not product:
        raise ProductNotFound()
    
    cart = await _get_or_create_cart(user_id,db)

    stmt = select(CartItem).where(CartItem.cart_id==cart.id,CartItem.product_id==payload.product_id)
    cart_item = await db.scalar(stmt)

    if cart_item:
        cart_item.quantity += payload.quantity

    else:
        cart_item = CartItem(
        cart_id = cart.id,
        product_id = payload.product_id,
        quantity = payload.quantity
        )
        db.add(cart_item)

    await db.commit()

    return await _build_cart_response(cart,db)


async def get_cart(user_id:int,db:AsyncSession)->CartResponse:
    cart = await _get_or_create_cart(user_id,db)

    return await _build_cart_response(cart,db)

# Receive user_id
#       │
#       ▼
# Get/Create Cart
#       │
#       ▼
# Find CartItem
# WHERE
# cart_id = user's cart
# AND
# id = item_id
#       │
#       ├── Not Found
#       │      │
#       │      ▼
#       │   Exception
#       │
#       ▼
# Update Quantity
#       │
#       ▼
# Commit
#       │
#       ▼
# Build Response

async def update_cart_item(user_id:int,item_id:int,db:AsyncSession,payload: CartItemUpdate)->CartResponse:
    cart = await _get_or_create_cart(user_id,db)

    stmt = select(CartItem).where(
    CartItem.cart_id == cart.id,
    CartItem.id == item_id,# if two or more conditions are there then treated as AND
    )
    item = await db.scalar(stmt)

    if not item:
        raise ItemNotFoundError()
    
    item.quantity = payload.quantity

    await db.commit()

    return await _build_cart_response(cart,db)

# Receive user_id
#       │
#       ▼
# Get/Create Cart
#       │
#       ▼
# Find CartItem
#       │
#       ├── Not Found
#       │
#       ▼
# Delete Item
#       │
#       ▼
# Commit

async def remove_cart_item(user_id:int,db:AsyncSession,item_id:int)->None:
    cart = await _get_or_create_cart(user_id,db)

    stmt = select(CartItem).where(
    CartItem.id == item_id,
    CartItem.cart_id == cart.id,
    )
    item = await db.scalar(stmt)

    if not item:
        raise ItemNotFoundError()
    
    await db.delete(item)
    await db.commit()

    return None

# This one is even easier.

# Receive user_id
#       │
#       ▼
# Get/Create Cart
#       │
#       ▼
# Delete ALL CartItems
# WHERE cart_id = ?
#       │
#       ▼
# Commit
async def clear_cart(user_id:int,db:AsyncSession)->None:
    cart = await _get_or_create_cart(user_id,db)

    stmt = select(CartItem).where(CartItem.cart_id == cart.id)
    items = (await db.scalars(stmt)).all()

    if not items:
        raise ItemNotFoundError()
    
    for item in items:
        await db.delete(item)
        
    await db.commit()
    return None

    # return none i know we can ignore this


