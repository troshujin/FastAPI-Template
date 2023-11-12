# pylint: skip-file

import pytest
from httpx import AsyncClient
from fastapi import Response


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    """Test to determine user was successfully created"""
    response: Response = await client.post(
        "/api/v1/users",
        json={"username": "user3", "password": "user3"}
    )
    assert response.status_code == 201

    data = response.json()
    assert data["username"] == "user3"


@pytest.mark.asyncio
async def test_get_users(client: AsyncClient, admin_token_headers: dict[str, str]):
    """Test to determine all the user information was successfully retrieved"""
    admin_headers = await admin_token_headers

    res = await client.get("/api/v1/users", headers=admin_headers)
    print(res.json())
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient, normal_user_token_headers: dict[str, str]):
    """Test to determine user information was successfully updated with new information"""
    user_headers = await normal_user_token_headers

    res = await client.patch("/api/v1/users/2", headers=user_headers, json={"username": "bla", "password": "bla"})
    assert res.status_code == 200, "Update user failed"

    assert res.json()["username"] == "bla"

    res = await client.patch("/api/v1/users/2", headers=user_headers, json={"username": "normal_user", "password": "normal_user"})
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient):
    """Test to determine user was successfully deleted from database"""
    login_data = {
        "username": "user3",
        "password": "user3"
    }
    response = await client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200, "Login failure"

    response = response.json()
    access_token = response["access_token"]

    res = await client.delete("/api/v1/users/3",headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 204
    

@pytest.mark.asyncio
async def test_create_existing_user(client: AsyncClient):
    """Test to determine whether user exists"""
    response: Response = await client.post(
        "/api/v1/users",
        json={"username": "admin", "password": "admin"}
    )

    assert response.status_code == 409
    

@pytest.mark.asyncio
async def test_get_users_no_auth(client: AsyncClient):
    """Test to determine whether users with no authorization access are able to retrieve unauthorized information"""
    res = await client.get("/api/v1/users")
    assert res.status_code == 401

