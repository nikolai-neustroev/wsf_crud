from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src import models, schemas, crud
from src.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/product_type/", response_model=schemas.ProductType)
def create_product_type(product_type: schemas.ProductTypeCreate, db: Session = Depends(get_db)):
    db_product_type = crud.get_product_type_by_name(db, name=product_type.name)
    if db_product_type:
        raise HTTPException(status_code=400, detail="Name already occupied")
    return crud.create_product_type(db=db, product_type=product_type)


@app.get("/product_types/", response_model=List[schemas.ProductType])
def read_product_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    product_types = crud.get_product_types(db, skip=skip, limit=limit)
    return product_types


@app.get("/product_type/name/{product_type_name}", response_model=schemas.ProductType)
def read_product_type_by_name(product_type_name: str, db: Session = Depends(get_db)):
    db_product_type = crud.get_product_type_by_name(db, name=product_type_name)
    if db_product_type is None:
        raise HTTPException(status_code=404, detail="Product type not found")
    return db_product_type


@app.get("/product_type/id/{product_type_id}", response_model=schemas.ProductType)
def read_product_type(product_type_id: int, db: Session = Depends(get_db)):
    db_product_type = crud.get_product_type_by_id(db, product_type_id=product_type_id)
    if db_product_type is None:
        raise HTTPException(status_code=404, detail="Product type not found")
    return db_product_type


@app.post("/product/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_name(db, name=product.name)
    if db_product:
        raise HTTPException(status_code=400, detail="Name already occupied")
    return crud.create_product(db=db, product=product)


@app.get("/products/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products


@app.get("/product/name/{product_name}", response_model=schemas.Product)
def read_product_by_name(product_name: str, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_name(db, name=product_name)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.get("/product/id/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product
