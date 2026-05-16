import json
import os
import sys
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = os.environ.get("DATABASE_URL")
if not db_url:
    print("Error: DATABASE_URL environment variable not set")
    sys.exit(1)

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from models import Employee

def load_employees():
    with open("employees_data.json", "r") as f:
        employees_data = json.load(f)

    db = SessionLocal()
    try:
        existing_count = db.query(Employee).count()
        print(f"Existing employees in database: {existing_count}")

        batch_size = 1000
        total = len(employees_data)

        for i in range(0, total, batch_size):
            batch = employees_data[i:i+batch_size]
            employees = []

            for emp in batch:
                employee = Employee(
                    first_name=emp["first_name"],
                    last_name=emp["last_name"],
                    full_name=emp["full_name"],
                    job_title=emp["job_title"],
                    country=emp["country"],
                    salary=emp["salary"],
                    mobile_number=emp["mobile_number"],
                    email=emp["email"],
                    date_of_birth=datetime.fromisoformat(emp["date_of_birth"]),
                    date_of_joining=datetime.fromisoformat(emp["date_of_joining"]),
                )
                employees.append(employee)

            db.bulk_save_objects(employees)
            db.commit()
            print(f"Inserted {min(i+batch_size, total)}/{total} employees")

        print(f"Successfully seeded {total} employees")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    load_employees()