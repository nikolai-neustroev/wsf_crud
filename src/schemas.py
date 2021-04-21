import re
from datetime import datetime
from typing import List

from pydantic import BaseModel, validator


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


class TransactionBase(BaseModel):
    recipient: str

    @validator('recipient')
    def is_right_length(cls, v):
        if len(v) < 11:
            raise ValueError('Recipient code is too short.')
        elif len(v) > 11:
            raise ValueError('Recipient code is too long.')
        return v

    @validator('recipient')
    def is_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Only letters and numbers are allowed.')
        return v

    @validator('recipient')
    def contains_letters(cls, v):
        if re.match('[а-яА-Я]', v[0:2]) is None:
            raise ValueError('The first two symbols should be Cyrillic.')
        if re.match('[а-яА-Я]', v[8:10]) is None:
            raise ValueError('Two symbols after date should be Cyrillic.')
        return v

    @validator('recipient')
    def contains_date(cls, v):
        try:
            datetime.strptime(v[2:8], '%d%m%y')
        except ValueError:
            raise ValueError('Date is not found.')
        return v

    @validator('recipient')
    def contains_gender(cls, v):
        if re.match('ж|Ж|м|М', v[10]) is None:
            raise ValueError('The last symbol should be Ж or М')
        return v


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int

    class Config:
        orm_mode = True


class CartBase(BaseModel):
    product_id: int
    quantity: int

    @validator('quantity')
    def is_gt_zero(cls, v):
        if v <= 0:
            raise ValueError('Quantity should be greater than 0.')
        return v


class CartCreate(CartBase):
    pass


class Cart(CartBase):
    id: int
    transaction_id: Transaction

    class Config:
        orm_mode = True
