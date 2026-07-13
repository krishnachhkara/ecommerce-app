from sqlalchemy import Integer,String,ForeignKey,Numeric,func,DateTime
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.base import Base
from typing import TYPE_CHECKING
from decimal import Decimal
from enum import Enum
from datetime import datetime
from sqlalchemy import Enum as SQLEnum

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.product import Product

class PaymentMethod(str,Enum):
    COD ="cod"
    STRIPE = "stripe"
    RAZORPAY = 'razorpay'

class OrderStatus(str,Enum):
    PENDING = "pending"
    PROCESSING="processing"
    SHIPPED="shipped"
    DELIVERED="delivered"
    CANCELLED="cancelled"

class Order(Base):
    __tablename__ = 'orders'
    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    user_id:Mapped[int] = mapped_column(Integer,ForeignKey("users.id"),nullable=False)
    total_amount:Mapped[Decimal] = mapped_column(Numeric(10,2),nullable=False)
    payment_method:Mapped[PaymentMethod] = mapped_column(SQLEnum(PaymentMethod),default=PaymentMethod.COD,nullable=False)
    status:Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus),default=OrderStatus.PENDING,nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())

    #relations
    user:Mapped["User"] = relationship(back_populates="orders")
    items:Mapped[list["OrderItem"]] = relationship(back_populates="order",cascade="all,delete-orphan")


# Har Order ek hi User ka hota hai.
#
# order.user se us Order ka owner User object mil jayega.
#
# back_populates="orders"
# batata hai ki User model me "orders" relationship iska opposite side hai.
# user: Mapped["User"] = relationship(
#     back_populates="orders"
# )

class OrderItem(Base):
    __tablename__ = "order_items"
    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    order_id:Mapped[int] = mapped_column(Integer,ForeignKey("orders.id"),nullable=False)
    product_id:Mapped[int] = mapped_column(Integer,ForeignKey("products.id"),nullable=False)
    size:Mapped[str] = mapped_column(String,nullable=False)
    quantity:Mapped[int] = mapped_column(Integer,default=1,nullable=False)
    price:Mapped[Decimal] = mapped_column(Numeric(10,2),nullable=False) 

    #relations
    order:Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship(back_populates="order_items")

# Har OrderItem ek specific Order ka part hota hai.
#
# order_item.order se parent Order mil jata hai.
#
# Example:
# Nike Shirt (OrderItem)
#          ↓
# Order #101
#
# back_populates="items"
# batata hai ki Order model me "items" relationship iska opposite side hai.
# order: Mapped["Order"] = relationship(
#     back_populates="items"
# )


# Har OrderItem ek specific Product ko represent karta hai.
#
# order_item.product se purchased Product object mil jata hai.
#
# Example:
# OrderItem
#      ↓
# Nike Shirt
#
# Note:
# Price OrderItem me alag store ki gayi hai taaki future me Product ki
# price change hone par old orders ka record na badle.
#
# back_populates="order_items"
# batata hai ki Product model me "order_items" relationship iska opposite side hai.
# product: Mapped["Product"] = relationship(
#     back_populates="order_items"
# )
