import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime


class TestCreateEmployee:
    """Test suite for creating employees"""

    @pytest.fixture
    def mock_employee_data(self):
        return {
            "first_name": "John",
            "last_name": "Doe",
            "full_name": "John Doe",
            "job_title": "Software Engineer",
            "country": "USA",
            "salary": 75000.00,
            "mobile_number": "+1234567890",
            "email": "john.doe@example.com",
            "date_of_birth": "1990-01-15",
            "date_of_joining": "2023-06-01"
        }

    def test_create_employee_success(self, mock_employee_data):
        """Test that creating an employee succeeds"""
        mock_session = MagicMock()
        mock_session.add = MagicMock()
        mock_session.commit = MagicMock()
        
        created_employee = MagicMock()
        created_employee.id = 1
        created_employee.first_name = "John"
        created_employee.last_name = "Doe"
        created_employee.full_name = "John Doe"
        created_employee.job_title = "Software Engineer"
        created_employee.country = "USA"
        created_employee.salary = 75000.00
        created_employee.mobile_number = "+1234567890"
        created_employee.email = "john.doe@example.com"
        created_employee.date_of_birth = datetime(1990, 1, 15)
        created_employee.date_of_joining = datetime(2023, 6, 1)
        created_employee.created_at = datetime(2023, 6, 1)
        created_employee.updated_at = None
        mock_session.refresh = MagicMock(side_effect=lambda x: setattr(x, 'id', 1))
        
        def mock_get_db():
            yield mock_session
            
        with patch("appSettings.get_db", mock_get_db):
            with patch("employees.Employee", return_value=created_employee):
                from main import app
                from fastapi.testclient import TestClient

                client = TestClient(app)
                response = client.post("/api/employees", json=mock_employee_data)

                assert response.status_code == 200
                data = response.json()
                assert data["first_name"] == "John"
                assert data["last_name"] == "Doe"
                assert data["full_name"] == "John Doe"
                assert data["job_title"] == "Software Engineer"

    def test_create_employee_validates_required_fields(self):
        """Test that creating employee validates required fields"""
        def mock_get_db():
            yield MagicMock()
            
        with patch("appSettings.get_db", mock_get_db):
            from main import app
            from fastapi.testclient import TestClient

            client = TestClient(app)
            response = client.post("/api/employees", json={})
            assert response.status_code == 422


class TestGetEmployees:
    """Test suite for getting employees"""

    def test_get_employees_returns_empty_list_when_no_data(self):
        """Test that getting employees returns empty list when no employees"""
        mock_session = MagicMock()
        mock_query = MagicMock()
        mock_query.all.return_value = []
        mock_session.query.return_value = mock_query

        def mock_get_db():
            yield mock_session
            
        with patch("appSettings.get_db", mock_get_db):
            from main import app
            from fastapi.testclient import TestClient

            client = TestClient(app)
            response = client.get("/api/employees")

            assert response.status_code == 200
            data = response.json()
            assert data == []


class TestDeleteEmployee:
    """Test suite for deleting employees"""

    @pytest.fixture
    def mock_existing_employee(self):
        emp = MagicMock()
        emp.id = 1
        emp.first_name = "John"
        emp.last_name = "Doe"
        emp.full_name = "John Doe"
        emp.job_title = "Software Engineer"
        emp.country = "USA"
        emp.salary = 75000.00
        emp.mobile_number = "+1234567890"
        emp.email = "john.doe@example.com"
        emp.date_of_birth = datetime(1990, 1, 15)
        emp.date_of_joining = datetime(2023, 6, 1)
        return emp

    def test_delete_employee_success(self, mock_existing_employee):
        """Test that deleting an employee succeeds"""
        mock_session = MagicMock()
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_filter.first.return_value = mock_existing_employee
        mock_query.filter.return_value = mock_filter
        mock_session.query.return_value = mock_query
        mock_session.delete = MagicMock()
        mock_session.commit = MagicMock()

        def mock_get_db():
            yield mock_session
            
        with patch("appSettings.get_db", mock_get_db):
            from main import app
            from fastapi.testclient import TestClient

            client = TestClient(app)
            response = client.delete("/api/employees/1")

            assert response.status_code == 200
            assert "message" in response.json()