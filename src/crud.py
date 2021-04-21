from sqlalchemy.orm import Session

from src import models, schemas


def get_product_type_by_id(db: Session, product_type_id: int):
    return db.query(models.ProductType).get(product_type_id)


def get_product_type_by_name(db: Session, name: str):
    return db.query(models.ProductType).filter(models.ProductType.name == name).first()


def get_product_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ProductType).offset(skip).limit(limit).all()


def create_product_type(db: Session, product_type: schemas.ProductType):
    db_product_type = models.ProductType(name=product_type.name)
    db.add(db_product_type)
    db.commit()
    db.refresh(db_product_type)
    return db_product_type


def get_product(db: Session, product_id: int):
    return db.query(models.Product).get(product_id)


def get_product_by_name(db: Session, name: str):
    return db.query(models.Product).filter(models.Product.name == name).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.Product):
    db_product = models.Product(name=product.name, product_type_id=product.product_type_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
