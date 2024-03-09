import pytest
from unittest.mock import MagicMock
from database.models import User


def test_signup_user(client, user, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("services.email.send_email", mock_send_email)
    response = client.post("/auth/signup", json=user)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["user"]["email"] == user.get("email")
    assert "id" in data["user"]


def test_signup_user_twice(client, user):
    response = client.post("/auth/signup", json=user)
    assert response.status_code == 409, response.text
    data = response.json()
    assert data["detail"] == "Account already exists"


def test_login_user_not_confirmed(client, user, session):
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.verified = False
    response = client.post("/auth/login", data={"username": user.get("email"), "password": user.get("password")})
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == ("Email not confirmed")


def test_login_user(client, user, session):
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.verified = True
    session.commit()
    response = client.post("/auth/login", data={"username": user.get("email"), "password": user.get("password")})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["token_type"] == "bearer"


def test_login_user_wrong_password(client, user):
    response = client.post("/auth/login", data={"username": user.get('email'), "password": 'password'})
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid password"


def test_login_wrong_email(client, user):
    response = client.post("/auth/login", data={"username": 'email', "password": user.get('password')})
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid email"


if __name__ == "__main__":
    pytest.main(["-v", "test_route_auth.py"])
