import pytest
from unittest.mock import MagicMock, patch


class TestSignup:
    """Test suite for signup endpoint"""

    @pytest.fixture
    def mock_session(self):
        mock_sess = MagicMock()
        mock_sess.query.return_value.filter.return_value.first.return_value = None
        return mock_sess

    def test_signup_creates_new_user(self, mock_session):
        """Test that signup creates a new user with correct data"""
        with patch("main.SessionLocal", return_value=mock_session):
            with patch("main.pwd_context") as mock_pwd:
                mock_pwd.hash.return_value = "hashed_password"
                mock_pwd.verify.return_value = True

                from main import app
                from fastapi.testclient import TestClient

                client = TestClient(app)
                response = client.post("/api/signup", json={
                    "username": "newuser",
                    "password": "password123",
                    "name": "New User"
                })

                assert response.status_code == 200
                data = response.json()
                assert data["user"]["username"] == "newuser"
                assert data["user"]["name"] == "New User"
                assert data["user"]["role"] == "user"
                assert "access_token" in data

    def test_signup_fails_for_existing_username(self, mock_session):
        """Test that signup fails when username already exists"""
        existing_user = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = existing_user

        with patch("main.SessionLocal", return_value=mock_session):
            from main import app
            from fastapi.testclient import TestClient

            client = TestClient(app)
            response = client.post("/api/signup", json={
                "username": "existinguser",
                "password": "password123",
                "name": "Existing User"
            })

            assert response.status_code == 400
            assert "Username already exists" in response.json()["detail"]

    def test_signup_validates_required_fields(self):
        """Test that signup validates required fields"""
        from main import app
        from fastapi.testclient import TestClient
        from fastapi import FastAPI
        from sqlalchemy.orm import Session

        with patch("main.SessionLocal") as mock_session_local:
            mock_db = MagicMock(spec=Session)
            mock_session_local.return_value = mock_db

            with patch("main.get_db", return_value=iter([mock_db])):
                client = TestClient(app)

                response = client.post("/api/signup", json={"username": "test"})
                assert response.status_code == 422

                response = client.post("/api/signup", json={"password": "test"})
                assert response.status_code == 422

                response = client.post("/api/signup", json={"name": "test"})
                assert response.status_code == 422

    def test_signup_returns_jwt_token(self, mock_session):
        """Test that signup returns a valid JWT token"""
        with patch("main.SessionLocal", return_value=mock_session):
            with patch("main.pwd_context") as mock_pwd:
                mock_pwd.hash.return_value = "hashed_password"

                from main import app
                from fastapi.testclient import TestClient

                client = TestClient(app)
                response = client.post("/api/signup", json={
                    "username": "tokenuser",
                    "password": "password123",
                    "name": "Token User"
                })

                assert response.status_code == 200
                data = response.json()
                assert "access_token" in data
                assert data["token_type"] == "bearer"


class TestLogin:
    """Test suite for login endpoint"""

    @pytest.fixture
    def mock_session_with_user(self):
        mock_session = MagicMock()
        user_obj = MagicMock()
        user_obj.username = "testuser"
        user_obj.password_hash = "$2b$12$hashedpassword"
        user_obj.name = "Test User"
        user_obj.role = "user"
        mock_session.query.return_value.filter.return_value.first.return_value = user_obj
        return mock_session

    def test_login_success_with_valid_credentials(self, mock_session_with_user):
        """Test that login succeeds with valid credentials"""
        with patch("main.SessionLocal", return_value=mock_session_with_user):
            with patch("main.pwd_context") as mock_pwd:
                mock_pwd.verify.return_value = True

                from main import app
                from fastapi.testclient import TestClient

                client = TestClient(app)
                response = client.post("/api/login", json={
                    "username": "testuser",
                    "password": "password123"
                })

                assert response.status_code == 200
                data = response.json()
                assert data["user"]["username"] == "testuser"
                assert "access_token" in data

    def test_login_fails_with_invalid_username(self):
        """Test that login fails with non-existent username"""
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = None

        with patch("main.SessionLocal", return_value=mock_session):
            from main import app
            from fastapi.testclient import TestClient

            client = TestClient(app)
            response = client.post("/api/login", json={
                "username": "nonexistent",
                "password": "password123"
            })

            assert response.status_code == 401
            assert "Invalid username or password" in response.json()["detail"]

    def test_login_fails_with_invalid_password(self, mock_session_with_user):
        """Test that login fails with incorrect password"""
        with patch("main.SessionLocal", return_value=mock_session_with_user):
            with patch("main.pwd_context") as mock_pwd:
                mock_pwd.verify.return_value = False

                from main import app
                from fastapi.testclient import TestClient

                client = TestClient(app)
                response = client.post("/api/login", json={
                    "username": "testuser",
                    "password": "wrongpassword"
                })

                assert response.status_code == 401
                assert "Invalid username or password" in response.json()["detail"]

    def test_login_validates_required_fields(self):
        """Test that login validates required fields"""
        from main import app
        from fastapi.testclient import TestClient
        from sqlalchemy.orm import Session

        with patch("main.SessionLocal") as mock_session_local:
            mock_db = MagicMock(spec=Session)
            mock_session_local.return_value = mock_db

            with patch("main.get_db", return_value=iter([mock_db])):
                client = TestClient(app)

                response = client.post("/api/login", json={"username": "test"})
                assert response.status_code == 422

                response = client.post("/api/login", json={"password": "test"})
                assert response.status_code == 422


class TestLogout:
    """Test suite for logout endpoint"""

    def test_logout_returns_success_message(self):
        """Test that logout returns success message"""
        from main import app
        from fastapi.testclient import TestClient

        client = TestClient(app)
        response = client.post("/api/logout")

        assert response.status_code == 200
        assert response.json() == {"message": "Logged out successfully"}


class TestGetCurrentUser:
    """Test suite for get current user endpoint"""

    def test_get_current_user_with_valid_token(self):
        """Test that /api/me returns user info with valid token"""
        from main import app
        from fastapi.testclient import TestClient
        import jwt
        from main import SECRET_KEY, ALGORITHM

        client = TestClient(app)
        token = jwt.encode({"sub": "testuser", "name": "Test User", "role": "user"}, SECRET_KEY, algorithm=ALGORITHM)

        client.cookies.set("access_token", token)
        response = client.get("/api/me")

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"

    def test_get_current_user_without_token(self):
        """Test that /api/me returns 401 without token"""
        from main import app
        from fastapi.testclient import TestClient

        client = TestClient(app)
        response = client.get("/api/me")

        assert response.status_code == 401

    def test_get_current_user_with_invalid_token(self):
        """Test that /api/me returns 401 with invalid token"""
        from main import app
        from fastapi.testclient import TestClient

        client = TestClient(app)
        client.cookies.set("access_token", "invalid-token")
        response = client.get("/api/me")

        assert response.status_code == 401