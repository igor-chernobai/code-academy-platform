import pytest
from django.contrib.auth import get_user_model
from rest_framework import status


@pytest.mark.django_db
def test_register_success(api_client):
    email, first_name, password = "authtestuser@gmail.com", "Test User", "test_user"

    data = {"email": email, "first_name": first_name, "password": password, "password2": password}
    response = api_client.post("/api/auth/register/", data=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["email"] == "authtestuser@gmail.com"
    assert "password" not in response.data
    assert "password2" not in response.data
    assert response.data["first_name"] == first_name
    assert get_user_model().objects.filter(email=email).exists()


@pytest.mark.django_db
def test_register_passwords_do_not_match(api_client):
    email, first_name, password = "authtestuser@gmail.com", "Test User", "test_user"
    invalid_data = {
        "email": email,
        "first_name": first_name,
        "password": password,
        "password2": "invalidpassord",
    }
    response = api_client.post("/api/auth/register/", invalid_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not get_user_model().objects.filter(email=email).exists()


@pytest.mark.django_db
def test_register_duplicate_email(api_client, user):
    data = {
        "email": user.email,
        "first_name": "Test User",
        "password": "testuser",
        "password2": "testuser",
    }
    response = api_client.post("/api/auth/register/", data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data
    assert get_user_model().objects.filter(email=user.email).count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize("field_name", ["email", "first_name", "password", "password2"])
def test_register_missing_required_fields(api_client, field_name):
    data = {
        "email": "test_user@gmail.com",
        "first_name": "Test User",
        "password": "testuser",
        "password2": "testuser",
    }
    data.pop(field_name)
    response = api_client.post("/api/auth/register/", data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert field_name in response.data


def test_user_can_login(api_client, user):
    data = {"email": user.email, "password": "12345789"}
    response = api_client.post("/api/token/", data)

    assert response.status_code == status.HTTP_200_OK
    assert "refresh" in response.data
    assert "access" in response.data


def test_user_cannot_login_with_wrong_password(api_client, user):
    data = {"email": user.email, "password": "invalid_password"}
    response = api_client.post("/api/token/", data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_cannot_login_with_wrong_email(api_client, user):
    data = {"email": "wrong@example.com", "password": "invalid_password"}
    response = api_client.post("/api/token/", data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_cannot_login_without_email(api_client):
    data = {"password": "some_password"}
    response = api_client.post("/api/token/", data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_user_cannot_login_without_password(api_client, user):
    data = {"email": user.email}
    response = api_client.post("/api/token/", data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_user_can_refresh_token(api_client, user):
    user_data = {"email": user.email, "password": "12345789"}
    response_login = api_client.post("/api/token/", user_data)
    response = api_client.post("/api/token/refresh/", {"refresh": response_login.data["refresh"]})

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data


def test_user_can_verify_access_token(api_client, user):
    user_data = {"email": user.email, "password": "12345789"}
    response_login = api_client.post("/api/token/", user_data)
    response = api_client.post("/api/token/verify/", {"token": response_login.data["access"]})

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "payload, expected_status",
    [
        ({"token": "invalid-token"}, status.HTTP_401_UNAUTHORIZED),
        ({}, status.HTTP_400_BAD_REQUEST),
        ({"token": ""}, status.HTTP_400_BAD_REQUEST),
    ],
)
def test_user_cannot_verify_invalid_token(api_client, payload, expected_status):
    response = api_client.post("/api/token/verify/", payload)

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "payload, expected_status",
    [
        ({"refresh": "invalid-token"}, status.HTTP_401_UNAUTHORIZED),
        ({}, status.HTTP_400_BAD_REQUEST),
        ({"refresh": ""}, status.HTTP_400_BAD_REQUEST),
    ],
)
def test_refresh_token_invalid_cases(api_client, payload, expected_status):
    response = api_client.post("/api/token/refresh/", payload)

    assert response.status_code == expected_status
