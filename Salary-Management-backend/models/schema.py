from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class SignupRequest(BaseModel):
    username: str
    password: str
    name: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict


class EmployeeRequest(BaseModel):
    first_name: str
    last_name: str
    full_name: str
    job_title: str
    country: str
    salary: float
    mobile_number: str
    email: str
    date_of_birth: str
    date_of_joining: str


class EmployeeResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    full_name: str
    job_title: str
    country: str
    salary: float
    mobile_number: str
    email: str
    date_of_birth: str
    date_of_joining: str
    created_at: str
    updated_at: str | None = None

    class Config:
        from_attributes = True


class PaginatedEmployeesResponse(BaseModel):
    data: list[EmployeeResponse]
    total: int
    page: int
    limit: int
    total_pages: int