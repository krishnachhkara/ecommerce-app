from decimal import Decimal
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    func,
)
<<<<<<< HEAD
=======
from sqlalchemy.dialects.postgresql import ARRAY
>>>>>>> 4e815fb (feat: implement product and cart modules)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:

    from app.models.cart import CartItem
    from app.models.orders import Order,OrderItem
<<<<<<< HEAD
=======
    from app.models.cart import Cart,CartItem
>>>>>>> 4e815fb (feat: implement product and cart modules)


# here the mapped part is for python and mappedcol is for database(type storing in python and database)
#  id: Mapped[int] = mapped_column(primary_key=True)


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

<<<<<<< HEAD
=======
    sizes: Mapped[list[str]] = mapped_column(
    ARRAY(String),
    nullable=False
    )

>>>>>>> 4e815fb (feat: implement product and cart modules)
    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    subcategory: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    bestseller: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


    #relations

    # One Product -> Many Images
    images: Mapped[list["ProductImage"]] = relationship(back_populates="product",cascade="all, delete-orphan")

    cart_items:Mapped[list["CartItem"]] = relationship(back_populates="product",cascade='all, delete-orphan')
    order_items:Mapped[list["OrderItem"]] = relationship(back_populates="product")


# Ek Product ki multiple images ho sakti hain.
# relationship ki wajah se product.images se us product ki saari images access kar sakte hain.
#
# Example:
# Nike Shirt
# ├── image1.jpg
# ├── image2.jpg
# └── image3.jpg
#
# back_populates="product"
# batata hai ki ProductImage model me "product" relationship iska opposite side hai.
#
# cascade="all, delete-orphan"
# agar Product delete ho gaya to uski saari images bhi delete ho jayengi.
# orphan ka matlab: agar image kisi Product se linked na rahe to SQLAlchemy usse delete kar dega.
# images: Mapped[list["ProductImage"]] = relationship(
#     back_populates="product",
#     cascade="all, delete-orphan"
# )


# Ek Product multiple users ke cart me ho sakta hai.
#
# product.cart_items se pata chal sakta hai ki kitne cart entries
# is product ko refer kar rahe hain.
#
# Example:
# Nike Shirt
# ├── User A Cart
# ├── User B Cart
# └── User C Cart
#
# back_populates="product"
# batata hai ki CartItem model me "product" relationship iska opposite side hai.
# product_cart_items: Mapped[list["CartItem"]] = relationship(
#     back_populates="product"
# )


# Ek Product kai alag-alag orders me purchase kiya ja sakta hai.
#
# product.order_items se us product ki purchase history track ki ja sakti hai.
#
# Example:
# Nike Shirt
# ├── Order #101
# ├── Order #205
# └── Order #876
#
# back_populates="product"
# batata hai ki OrderItem model me "product" relationship iska opposite side hai.
# order_items: Mapped[list["OrderItem"]] = relationship(
#     back_populates="product"
# )




class ProductImage(Base):
    __tablename__ = "product_images"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )

    image_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

<<<<<<< HEAD
=======
    is_primary: Mapped[bool] = mapped_column(
    Boolean,
    default=False,
    nullable=False
)

>>>>>>> 4e815fb (feat: implement product and cart modules)
    # Many Images -> One Product
    product: Mapped["Product"] = relationship(back_populates="images")


    # Har ProductImage sirf ek Product se belong karti hai.
#
# image.product se parent Product object mil jayega.
#
# Example:
# image1.jpg
#      ↓
# Nike Shirt
#
# back_populates="images"
# batata hai ki Product model me "images" relationship iska opposite side hai.
# product: Mapped["Product"] = relationship(
#     back_populates="images"
# )