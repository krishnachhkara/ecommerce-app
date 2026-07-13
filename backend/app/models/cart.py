<<<<<<< HEAD
from sqlalchemy import Integer,String,ForeignKey,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.product import Product
=======
from sqlalchemy import Integer,ForeignKey,func,DateTime,UniqueConstraint,CheckConstraint
from sqlalchemy.orm import mapped_column,Mapped,relationship
from app.db.base import Base
from app.models.user import User
from app.models.product import Product
from datetime import datetime



class Cart(Base):
    __tablename__ = "carts"

    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    user_id:Mapped[int] = mapped_column(Integer,ForeignKey("users.id",ondelete="CASCADE"),unique=True,nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=func.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)

    #relationships
    user:Mapped["User"] = relationship(back_populates="cart")
    items:Mapped[list["CartItem"]] = relationship(back_populates="cart",cascade="all,delete-orphan")
>>>>>>> 4e815fb (feat: implement product and cart modules)



class CartItem(Base):
<<<<<<< HEAD
    __tablename__ = "cart_items"# no relation with relationship names 

    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    user_id:Mapped[int] = mapped_column(Integer,ForeignKey("users.id"),nullable=False)
    product_id:Mapped[int] = mapped_column(Integer,ForeignKey("products.id"),nullable=False)
    size:Mapped[str] = mapped_column(String,nullable=False)
    quantity:Mapped[int] = mapped_column(Integer,default=1,nullable=False)

    #relations
    user:Mapped["User"] = relationship(back_populates="cart_items")
    product:Mapped["Product"] = relationship(back_populates="cart_items")

    __table_args__ = (UniqueConstraint(
        "user_id","product_id","size",name="uq_cart_user_product_size"
    ),
    )
=======
    __tablename__ = "cart_items"

    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    cart_id:Mapped[int] = mapped_column(Integer,ForeignKey("carts.id",ondelete="CASCADE"),nullable=False)
    product_id:Mapped[int] = mapped_column(Integer,ForeignKey("products.id",ondelete="CASCADE"),nullable=False)

    quantity:Mapped[int] = mapped_column(Integer,nullable=False,server_default="1")

    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)

    #relationship
    cart:Mapped["Cart"] = relationship(back_populates="items")
    product:Mapped["Product"] = relationship(back_populates="cart_items")
    
        
    __table_args__ = (
    UniqueConstraint(
        "cart_id",
        "product_id",
        name="uq_cart_product"
    ),
    CheckConstraint(
    "quantity > 0",
    name="ck_cart_quantity_positive"
    )
    )

>>>>>>> 4e815fb (feat: implement product and cart modules)


# Har CartItem ek hi User ka hota hai.
#
# cart_item.user se us cart item ka owner User mil jayega.
#
# Example:
# Nike Shirt (CartItem)
#         ↓
# Krishna (User)
#
# back_populates="cart_items"
# batata hai ki User model me "cart_items" relationship iska opposite side hai.
# user: Mapped["User"] = relationship(
#     back_populates="cart_items"
# )    


# Har CartItem ek hi Product ko refer karta hai.
#
# cart_item.product se actual Product object mil jata hai.
#
# Example:
# CartItem
#     ↓
# Nike Shirt
#
# back_populates="cart_items"
# batata hai ki Product model me "cart_items" relationship iska opposite side hai.
# product: Mapped["Product"] = relationship(
#     back_populates="cart_items"
# )
