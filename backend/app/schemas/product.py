from pydantic import BaseModel,ConfigDict,Field
from decimal import Decimal

# return a image used to display on the product/product id page 
class ProductImageResponse(BaseModel):
    id: int
    image_url: str
    is_primary: bool

    model_config = ConfigDict(
        from_attributes=True
    )


#for creating the product 
class ProductCreate(BaseModel):
    name:str =  Field(min_length=3,max_length=150)
    description: str = Field(min_length=10,max_length=5000)
    price: Decimal = Field(gt=0,decimal_places=2)
    category: str
    subcategory: str
    sizes: list[str]
    bestseller: bool = False


# for collection,products,home page single product display
class ProductListResponse(BaseModel):
    id: int
    name: str
    price: Decimal
    image_url: str

    model_config = ConfigDict(
        from_attributes=True
    )    


# used to give detail response when on products/product id page i.e
# single product opened
class ProductDetailResponse(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    category: str
    subcategory: str
    sizes: list[str]
    bestseller: bool

    images: list[ProductImageResponse]

    model_config = ConfigDict(
        from_attributes=True
    )    

class ProductCreateResponse(BaseModel):
    id:int

# to update the product if anything there needs update
class ProductUpdate(BaseModel):
    name: str | None = Field(default=None,min_length=3,max_length=150)
    description: str | None = Field(default=None,min_length=10,max_length=5000)
    price: Decimal | None = Field(default=None,gt=0,decimal_places=2)
    category: str | None = None
    subcategory: str | None = None
    sizes: list[str] | None = None
    bestseller: bool | None = None    