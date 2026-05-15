import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient


@pytest.fixture
def mock_db_session():
    mock_session = MagicMock()
    return mock_session


@pytest.fixture
def mock_user():
    return {
        "id": 1,
        "username": "testuser",
        "password_hash": "$2b$12$hashedpassword",
        "name": "Test User",
        "role": "user"
    }


@pytest.fixture
def client():
    with patch("main.SessionLocal") as mock_session:
        mock_db = MagicMock()
        mock_session.return_value = mock_db

        from main import app
        from fastapi.testclient import TestClient
        return TestClient(app)