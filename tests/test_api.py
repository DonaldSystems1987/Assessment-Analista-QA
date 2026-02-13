from fastapi.testclient import TestClient
from app.main import app, fake_db

client = TestClient(app)


def test_login_success():
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_failure():
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid credentials"


def test_create_product_requires_admin():
    
    token_resp = client.post("/auth/login", json={"username": "user", "password": "user123"})
    token = token_resp.json()["access_token"]
    
    response = client.post(
        "/products",
        json={"name": "TestProduct", "price": 10.0, "quantity": 5},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403  

def test_create_product_success():
   
    token_resp = client.post("/auth/login", json={"username": "admin", "password": "admin123"})
    token = token_resp.json()["access_token"]

    response = client.post(
        "/products",
        json={"name": "TestProduct", "price": 10.0, "quantity": 5},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "TestProduct"
    assert data["price"] == 10.0
    assert data["quantity"] == 5
    assert "id" in data

def test_list_products():
    token_resp = client.post("/auth/login", json={"username": "admin", "password": "admin123"})
    token = token_resp.json()["access_token"]

    response = client.get("/products", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_adjust_inventory_success():
    token_resp = client.post("/auth/login", json={"username": "admin", "password": "admin123"})
    token = token_resp.json()["access_token"]

    create_resp = client.post(
        "/products",
        json={"name": "AdjustProduct", "price": 5.0, "quantity": 5},
        headers={"Authorization": f"Bearer {token}"}
    )
    product_id = create_resp.json()["id"]

    
    response = client.post(
        "/inventory/adjust",
        json={"product_id": product_id, "adjustment": 3, "reason": "Stock correction"},
        headers={"Authorization": f"Bearer {token}"}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["new_quantity"] == 8
    assert data["adjustment"] == 3

def test_calculate_profit_margin():
    token_resp = client.post("/auth/login", json={"username": "admin", "password": "admin123"})
    token = token_resp.json()["access_token"]

    
    create_resp = client.post(
        "/products",
        json={"name": "MarginProduct", "price": 20.0, "quantity": 2},
        headers={"Authorization": f"Bearer {token}"}
    )
    product_id = create_resp.json()["id"]

    response = client.get(f"/products/{product_id}/profit-margin?cost=10", headers={"Authorization": f"Bearer {token}"})
    data = response.json()
    assert response.status_code == 200
    assert data["margin_percentage"] == 100.0
