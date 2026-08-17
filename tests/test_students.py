import pytest


def register_and_login(client, email, password, role):
    client.post(
        "/auth/register",
        json={"name": role.title(), "email": email, "password": password, "role": role},
    )
    response = client.post("/auth/login", data={"username": email, "password": password})
    return response.json()["access_token"]


@pytest.fixture
def admin_token(client):
    return register_and_login(client, "admin@test.com", "admin123", "ADMIN")


@pytest.fixture
def student_token(client):
    return register_and_login(client, "student@test.com", "student123", "STUDENT")


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_admin_can_create_student(client, admin_token):
    response = client.post(
        "/students/",
        json={"name": "S1", "email": "s1@test.com", "course": "CS", "year": 1},
        headers=auth_headers(admin_token),
    )
    assert response.status_code == 201


def test_admin_can_list_students(client, admin_token):
    client.post(
        "/students/",
        json={"name": "S1", "email": "s1@test.com", "course": "CS", "year": 1},
        headers=auth_headers(admin_token),
    )
    response = client.get("/students/", headers=auth_headers(admin_token))
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_admin_can_update_student(client, admin_token):
    create_resp = client.post(
        "/students/",
        json={"name": "S1", "email": "s1@test.com", "course": "CS", "year": 1},
        headers=auth_headers(admin_token),
    )
    student_id = create_resp.json()["id"]
    response = client.put(
        f"/students/{student_id}", json={"course": "AI"}, headers=auth_headers(admin_token)
    )
    assert response.status_code == 200
    assert response.json()["course"] == "AI"


def test_admin_can_delete_student(client, admin_token):
    create_resp = client.post(
        "/students/",
        json={"name": "S1", "email": "s1@test.com", "course": "CS", "year": 1},
        headers=auth_headers(admin_token),
    )
    student_id = create_resp.json()["id"]
    response = client.delete(f"/students/{student_id}", headers=auth_headers(admin_token))
    assert response.status_code == 204


def test_student_cannot_create_student(client, student_token):
    response = client.post(
        "/students/",
        json={"name": "S1", "email": "s1@test.com", "course": "CS", "year": 1},
        headers=auth_headers(student_token),
    )
    assert response.status_code == 403


def test_student_cannot_delete_student(client, admin_token, student_token):
    create_resp = client.post(
        "/students/",
        json={"name": "S1", "email": "s1@test.com", "course": "CS", "year": 1},
        headers=auth_headers(admin_token),
    )
    student_id = create_resp.json()["id"]
    response = client.delete(f"/students/{student_id}", headers=auth_headers(student_token))
    assert response.status_code == 403


def test_student_can_view_students(client, admin_token, student_token):
    client.post(
        "/students/",
        json={"name": "S1", "email": "s1@test.com", "course": "CS", "year": 1},
        headers=auth_headers(admin_token),
    )
    response = client.get("/students/", headers=auth_headers(student_token))
    assert response.status_code == 200


def test_student_can_update_own_record(client, admin_token, student_token):
    me_resp = client.get("/auth/me", headers=auth_headers(student_token))
    student_user_id = me_resp.json()["id"]

    create_resp = client.post(
        "/students/",
        json={
            "name": "S1",
            "email": "s1@test.com",
            "course": "CS",
            "year": 1,
            "owner_id": student_user_id,
        },
        headers=auth_headers(admin_token),
    )
    student_record_id = create_resp.json()["id"]

    response = client.put(
        f"/students/{student_record_id}",
        json={"course": "AI"},
        headers=auth_headers(student_token),
    )
    assert response.status_code == 200
    assert response.json()["course"] == "AI"


def test_student_cannot_update_others_record(client, admin_token, student_token):
    create_resp = client.post(
        "/students/",
        json={"name": "S1", "email": "s1@test.com", "course": "CS", "year": 1},
        headers=auth_headers(admin_token),
    )
    student_record_id = create_resp.json()["id"]

    response = client.put(
        f"/students/{student_record_id}",
        json={"course": "AI"},
        headers=auth_headers(student_token),
    )
    assert response.status_code == 403