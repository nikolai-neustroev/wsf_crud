from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class ProductType(Base):
    __tablename__ = "tbl_product_type"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)

    products = relationship("Product", back_populates="product_type")


class Product(Base):
    __tablename__ = "tbl_product"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    product_type_id = Column(Integer, ForeignKey("tbl_product_type.id"))

    product_type = relationship("ProductType", back_populates="products")


class Transaction(Base):
    __tablename__ = "tbl_transaction"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    recipient = Column(String)
