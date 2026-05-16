from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Employee
from models.schema import EmployeeRequest, EmployeeResponse
from appSettings import get_db

router = APIRouter(prefix="/api/employees", tags=["employees"])


@router.get("", response_model=list[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    return [
        EmployeeResponse(
            id=e.id,
            first_name=e.first_name,
            last_name=e.last_name,
            full_name=e.full_name,
            job_title=e.job_title,
            country=e.country,
            salary=e.salary,
            mobile_number=e.mobile_number,
            email=e.email,
            date_of_birth=e.date_of_birth.isoformat() if e.date_of_birth else "",
            date_of_joining=e.date_of_joining.isoformat() if e.date_of_joining else "",
            created_at=e.created_at.isoformat() if e.created_at else "",
            updated_at=e.updated_at.isoformat() if e.updated_at else None,
        )
        for e in employees
    ]


@router.post("", response_model=EmployeeResponse)
def create_employee(request: EmployeeRequest, db: Session = Depends(get_db)):
    employee = Employee(
        first_name=request.first_name,
        last_name=request.last_name,
        full_name=request.full_name,
        job_title=request.job_title,
        country=request.country,
        salary=request.salary,
        mobile_number=request.mobile_number,
        email=request.email,
        date_of_birth=datetime.fromisoformat(request.date_of_birth),
        date_of_joining=datetime.fromisoformat(request.date_of_joining),
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return EmployeeResponse(
        id=employee.id,
        first_name=employee.first_name,
        last_name=employee.last_name,
        full_name=employee.full_name,
        job_title=employee.job_title,
        country=employee.country,
        salary=employee.salary,
        mobile_number=employee.mobile_number,
        email=employee.email,
        date_of_birth=employee.date_of_birth.isoformat() if employee.date_of_birth else "",
        date_of_joining=employee.date_of_joining.isoformat() if employee.date_of_joining else "",
        created_at=employee.created_at.isoformat() if employee.created_at else "",
        updated_at=employee.updated_at.isoformat() if employee.updated_at else None,
    )


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, request: EmployeeRequest, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise ValueError("Employee not found")
    
    employee.first_name = request.first_name
    employee.last_name = request.last_name
    employee.full_name = request.full_name
    employee.job_title = request.job_title
    employee.country = request.country
    employee.salary = request.salary
    employee.mobile_number = request.mobile_number
    employee.email = request.email
    employee.date_of_birth = datetime.fromisoformat(request.date_of_birth)
    employee.date_of_joining = datetime.fromisoformat(request.date_of_joining)
    
    db.commit()
    db.refresh(employee)
    return EmployeeResponse(
        id=employee.id,
        first_name=employee.first_name,
        last_name=employee.last_name,
        full_name=employee.full_name,
        job_title=employee.job_title,
        country=employee.country,
        salary=employee.salary,
        mobile_number=employee.mobile_number,
        email=employee.email,
        date_of_birth=employee.date_of_birth.isoformat() if employee.date_of_birth else "",
        date_of_joining=employee.date_of_joining.isoformat() if employee.date_of_joining else "",
        created_at=employee.created_at.isoformat() if employee.created_at else "",
        updated_at=employee.updated_at.isoformat() if employee.updated_at else None,
    )


@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise ValueError("Employee not found")
    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted successfully"}