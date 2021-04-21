import os

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..database import Base
from ..main import app, get_db
from ..utils import SQLALCHEMY_DATABASE_URL

engine = create_engine(
    os.environ[SQLALCHEMY_DATABASE_URL], connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_product_type():
    response = client.post(
        "/product_type/",
        json={"name": "Something"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Something"
    assert "id" in data
    product_type_id = data["id"]
    product_type_name = data["name"]

    response = client.get(f"/product_type/id/{product_type_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Something"
    assert data["id"] == product_type_id

    response = client.get(f"/product_type/name/{product_type_name}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Something"
    assert data["id"] == product_type_id


def test_read_product_types():
    client.post(
        "/product_type/",
        json={"name": "Something else"},
    )
    response = client.get("/product_types/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]['name'] == "Something"
    assert data[1]['name'] == "Something else"


def test_create_product():
    response = client.post("/product/", json={"name": "a name of a product", "product_type_id": 1})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['name'] == "a name of a product"
    assert data['product_type_id'] == 1
    assert data["id"] == 1
