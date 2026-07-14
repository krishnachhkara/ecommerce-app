from enum import Enum
from sqlalchemy import Integer,String,func,DateTime
from datetime import datetime
from sqlalchemy.orm import mapped_column,Mapped,relationship
from app.db.base import Base
from sqlalchemy import Enum as SQLEnum
from typing import TYPE_CHECKING
if TYPE_CHECKING:

    from app.models.cart import CartItem,Cart
    from app.models.orders import Order,OrderItem
    from app.models.refresh_token import RefreshToken



class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    name:Mapped[str] = mapped_column(String(255),nullable=False)
    email:Mapped[str] = mapped_column(String(255),index=True,nullable=False,unique=True)
    hashed_password:Mapped[str] = mapped_column(String,nullable=False)
    role:Mapped[UserRole] = mapped_column(SQLEnum(UserRole),default=UserRole.USER,nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())


    # realtions
    orders:Mapped[list["Order"]] = relationship(back_populates="user",cascade="all,delete-orphan")

    refresh_tokens:Mapped[list["RefreshToken"]] = relationship(back_populates="user",cascade="all,delete-orphan")
    cart:Mapped["Cart"] = relationship(back_populates="user",uselist=False)

# Ek User ke multiple Orders ho sakte hain.
# relationship ki wajah se user.orders se us user ke saare orders access kar sakte hain.
#
# back_populates="user"
# batata hai ki Order model me "user" relationship iska opposite side hai.
#
# cascade="all, delete-orphan"
# agar User delete ho gaya to uske saare Orders bhi delete ho jayenge.
# orphan ka matlab: agar koi Order apne User se disconnect ho jaye aur kisi User se linked na ho,
# to SQLAlchemy usse bhi delete kar dega.

# orders: Mapped[list["Order"]] = relationship(
#     back_populates="user",
#     cascade="all, delete-orphan"
# )


# Ek User ke cart me multiple items ho sakte hain.
#
# user.cart_items se us user ke cart ke saare products access kar sakte hain.
#
# Example:
# User
# ├── Nike Shirt
# ├── Puma Shoes
# └── Adidas Cap
#
# back_populates="user"
# batata hai ki CartItem model me "user" relationship iska opposite side hai.
#
# cascade="all, delete-orphan"
# agar User delete ho gaya to uske cart ke saare items bhi delete ho jayenge.
# cart_items: Mapped[list["CartItem"]] = relationship(
#     back_populates="user",
#     cascade="all, delete-orphan"
# )
