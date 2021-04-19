from typing import List

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    product_type_id: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


class ProductTypeBase(BaseModel):
    name: str


class ProductTypeCreate(ProductTypeBase):
    pass


class ProductType(ProductTypeBase):
    id: int
    products: List[Product] = []

    class Config:
        orm_mode = True
