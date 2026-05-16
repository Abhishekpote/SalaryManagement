import random
import json
from datetime import datetime, timedelta

first_names = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth",
    "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen",
    "Christopher", "Nancy", "Daniel", "Lisa", "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra",
    "Donald", "Ashley", "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
    "Kenneth", "Dorothy", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa", "Timothy", "Deborah",
    "Amit", "Priya", "Rahul", "Neha", "Sanjay", "Anita", "Vikram", "Sunita", "Rajesh", "Meera",
    "Wei", "Li", "Chen", "Zhang", "Ying", "Jian", "Hui", "Min", "Feng", "Ling",
    "Harry", "Sophie", "Oliver", "Emma", "Jack", "Olivia", "Thomas", "Ava", "William", "Isabella",
    "Hans", "Greta", "Klaus", "Ingrid", "Friedrich", "Brigitte", "Werner", "Ursula", "Wolfgang", "Elke",
    "Somsak", "Suda", "Krit", "Niran", "Thana", "Pichet", "Virat", "Kanyanat", "Nakorn", "Thip",
    "Kenji", "Yuki", "Hiroshi", "Sakura", "Takeshi", "Aiko", "Shinji", "Emiko", "Ryu", "Kaori",
    "Liam", "Chloe", "Noah", "Zoe", "Lucas", "Mia", "Ethan", "Charlotte", "Mason", "Aria"
]

last_names = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
    "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
    "Sharma", "Patel", "Kumar", "Singh", "Verma", "Gupta", "Joshi", "Khan", "Mehta", "Shah",
    "Wang", "Li", "Zhang", "Liu", "Yang", "Huang", "Zhao", "Wu", "Zhou", "Xu",
    "Taylor", "Brown", "Wilson", "Davies", "Robinson", "Wright", "Thompson", "White", "Hughes", "Edwards",
    "Mueller", "Schmidt", "Weber", "Fischer", "Meyer", "Wagner", "Becker", "Schulz", "Hoffmann", "Koch",
    "Chai", "Srisawat", "Prasert", "Kanjana", "Nakamura", "Tanaka", "Yamamoto", "Suzuki", "Watanabe", "Sato",
    "Jones", "Williams", "Brown", "Taylor", "Davies", "Wilson", "Evans", "Thomas", "Roberts", "Johnson"
]

job_titles = [
    "Software Engineer", "Senior Software Engineer", "Staff Engineer", "Principal Engineer", "Tech Lead",
    "Product Manager", "Senior Product Manager", "Project Manager", "Program Manager", "Scrum Master",
    "Data Scientist", "Senior Data Scientist", "Data Analyst", "Business Analyst", "BI Developer",
    "DevOps Engineer", "Site Reliability Engineer", "Cloud Engineer", "Security Engineer", "QA Engineer",
    "UI/UX Designer", "Graphic Designer", "Frontend Developer", "Backend Developer", "Full Stack Developer",
    "Database Administrator", "System Administrator", "Network Engineer", "IT Support Specialist", "Technical Writer",
    "HR Manager", "Recruiter", "Financial Analyst", "Accountant", "Marketing Manager", "Sales Representative",
    "Customer Success Manager", "Operations Manager", "Supply Chain Manager", "Logistics Coordinator",
    "CEO", "CTO", "CFO", "COO", "VP of Engineering", "VP of Product", "Director of Engineering",
    "Research Scientist", "Machine Learning Engineer", "AI Engineer", "Blockchain Developer", "Mobile Developer"
]

countries = ["India", "USA", "China", "UK", "Germany", "Thailand", "Japan", "Australia"]

def generate_phone():
    return f"+{random.randint(1, 999):03d}-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

def generate_date_of_birth():
    start_date = datetime(1970, 1, 1)
    end_date = datetime(2000, 12, 31)
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

def generate_date_of_joining():
    start_date = datetime(2010, 1, 1)
    end_date = datetime(2024, 12, 31)
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

def generate_salary(job_title):
    base_ranges = {
        "CEO": (200000, 500000),
        "CTO": (200000, 450000),
        "CFO": (200000, 450000),
        "COO": (180000, 400000),
        "VP": (150000, 350000),
        "Director": (120000, 250000),
        "Manager": (80000, 150000),
        "Senior": (90000, 180000),
        "Staff": (110000, 200000),
        "Principal": (130000, 220000),
        "Lead": (100000, 180000),
        "Engineer": (50000, 120000),
        "Developer": (45000, 100000),
        "Analyst": (45000, 90000),
        "Specialist": (40000, 80000),
        "Coordinator": (35000, 60000),
        "Representative": (35000, 70000),
        "Writer": (40000, 80000),
        "Support": (30000, 55000),
    }
    
    for key, range in base_ranges.items():
        if key.lower() in job_title.lower():
            return round(random.uniform(range[0], range[1]), 2)
    return round(random.uniform(40000, 120000), 2)

employees = []

for i in range(10000):
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    full_name = f"{first_name} {last_name}"
    
    domain = random.choice(["gmail.com", "yahoo.com", "outlook.com", "company.com", "techcorp.com"])
    email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@{domain}"
    
    employee = {
        "first_name": first_name,
        "last_name": last_name,
        "full_name": full_name,
        "job_title": random.choice(job_titles),
        "country": random.choice(countries),
        "salary": generate_salary(random.choice(job_titles)),
        "mobile_number": generate_phone(),
        "email": email,
        "date_of_birth": generate_date_of_birth(),
        "date_of_joining": generate_date_of_joining()
    }
    employees.append(employee)

with open("employees_data.json", "w") as f:
    json.dump(employees, f, indent=2)

print(f"Generated {len(employees)} employees in employees_data.json")