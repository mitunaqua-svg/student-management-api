def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={"name": "Admin", "email": "admin@test.com", "password": "admin123", "role": "ADMIN"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "admin@test.com"
    assert "password" not in data
    assert "password_hash" not in data


def test_register_duplicate_email(client):
    payload = {"name": "Admin", "email": "dup@test.com", "password": "admin123", "role": "ADMIN"}
    client.post("/auth/register", json=payload)
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400


def test_login_success(client):
    client.post(
        "/auth/register",
        json={"name": "Admin", "email": "admin@test.com", "password": "admin123", "role": "ADMIN"},
    )
    response = client.post("/auth/login", data={"username": "admin@test.com", "password": "admin123"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={"name": "Admin", "email": "admin@test.com", "password": "admin123", "role": "ADMIN"},
    )
    response = client.post("/auth/login", data={"username": "admin@test.com", "password": "wrongpass"})
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post("/auth/login", data={"username": "nouser@test.com", "password": "whatever"})
    assert response.status_code == 401


def test_protected_route_without_token(client):
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_protected_route_with_garbage_token(client):
    response = client.get("/auth/me", headers={"Authorization": "Bearer not.a.real.token"})
    assert response.status_code == 401