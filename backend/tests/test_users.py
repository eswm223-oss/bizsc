def test_create_user(client) -> None:
    response = client.post(
        "/users",
        json={
            "email": "test_create@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "test_create@example.com"
    assert data["is_active"] is True
    assert "id" in data

def test_get_user(client) -> None:
    create_response = client.post(
        "/users",
        json={
            "email": "test_get@example.com",
            "password": "password123",
        },
    )

    user_id = create_response.json()["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["email"] == "test_get@example.com"
    assert data["is_active"] is True

def test_update_user(client) -> None:
    create_response = client.post(
        "/users",
        json={
            "email": "test_update@example.com",
            "password": "password123",
        },
    )

    user_id = create_response.json()["id"]

    response = client.patch(
        f"/users/{user_id}",
        json={
            "email": "updated@example.com",
            "is_active": False,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["email"] == "updated@example.com"
    assert data["is_active"] is False


def test_delete_user(client) -> None:
    create_response = client.post(
        "/users",
        json={
            "email": "test_delete@example.com",
            "password": "password123",
        },
    )

    user_id = create_response.json()["id"]

    delete_response = client.delete(f"/users/{user_id}")

    assert delete_response.status_code == 204

    get_response = client.get(f"/users/{user_id}")

    assert get_response.status_code == 404