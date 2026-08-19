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


def test_get_users_with_search(client) -> None:
    client.post(
        "/users",
        json={
            "email": "alice@example.com",
            "password": "password123",
        },
    )
    client.post(
        "/users",
        json={
            "email": "bob@example.com",
            "password": "password123",
        },
    )

    response = client.get("/users?search=alice")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["users"]) == 1
    assert data["users"][0]["email"] == "alice@example.com"


def test_get_users_with_is_active_filter(client) -> None:
    client.post(
        "/users",
        json={
            "email": "bizscfilter20260819active@example.com",
            "password": "password123",
        },
    )

    inactive_response = client.post(
        "/users",
        json={
            "email": "bizscfilter20260819inactive@example.com",
            "password": "password123",
        },
    )

    inactive_user_id = inactive_response.json()["id"]

    client.patch(
        f"/users/{inactive_user_id}",
        json={
            "is_active": False,
        },
    )

    response = client.get(
        "/users?search=bizscfilter20260819&is_active=true"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["users"]) == 1
    assert data["users"][0]["email"] == "bizscfilter20260819active@example.com"
    assert data["users"][0]["is_active"] is True


def test_get_users_with_sort(client) -> None:
    client.post(
        "/users",
        json={
            "email": "bizscsortb@example.com",
            "password": "password123",
        },
    )

    client.post(
        "/users",
        json={
            "email": "bizscsorta@example.com",
            "password": "password123",
        },
    )

    response = client.get(
        "/users?search=bizscsort&sort_by=email&sort_order=asc"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert len(data["users"]) == 2
    assert data["users"][0]["email"] == "bizscsorta@example.com"
    assert data["users"][1]["email"] == "bizscsortb@example.com"


def test_get_users_with_pagination_and_total(client) -> None:
    for index in range(12):
        client.post(
            "/users",
            json={
                "email": f"bizscpage{index:02d}@example.com",
                "password": "password123",
            },
        )

    response = client.get(
        "/users?search=bizscpage&sort_by=email&sort_order=asc&page=2&limit=5"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 12
    assert len(data["users"]) == 5

    assert data["users"][0]["email"] == "bizscpage05@example.com"
    assert data["users"][4]["email"] == "bizscpage09@example.com"