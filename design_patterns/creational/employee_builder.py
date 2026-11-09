from dataclasses import dataclass
from typing import Optional


@dataclass
class Employee:
    first_name: str
    last_name: str
    email: str
    department: str
    position: str
    salary: float
    start_date: Optional[str] = None
    manager_id: Optional[int] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    has_parking: bool = False
    has_laptop: bool = False
    has_vpn_access: bool = False
    has_admin_rights: bool = False
    office_location: Optional[str] = None
    contract_type: str = "permanent"


class EmployeeBuilder:
    def __init__(self):
        self._data = {}

    def with_name(self, first_name, last_name):
        self._data["first_name"] = first_name
        self._data["last_name"] = last_name
        return self

    def with_email(self, email):
        self._data["email"] = email
        return self

    def with_job(self, department, position, salary):
        self._data["department"] = department
        self._data["position"] = position
        self._data["salary"] = salary
        return self

    def with_start_date(self, date):
        self._data["start_date"] = date
        return self

    def with_manager(self, manager_id):
        self._data["manager_id"] = manager_id
        return self

    def with_contact(self, phone=None, address=None, emergency_contact=None):
        self._data["phone"] = phone
        self._data["address"] = address
        self._data["emergency_contact"] = emergency_contact
        return self

    def with_equipment(self, laptop=False, parking=False):
        self._data["has_laptop"] = laptop
        self._data["has_parking"] = parking
        return self

    def with_access(self, vpn=False, admin=False):
        self._data["has_vpn_access"] = vpn
        self._data["has_admin_rights"] = admin
        return self

    def in_office(self, location):
        self._data["office_location"] = location
        return self

    def with_contract(self, contract_type):
        self._data["contract_type"] = contract_type
        return self

    def build(self):
        # all the validation is in one place now
        if not self._data.get("first_name") or not self._data.get("last_name"):
            raise ValueError("Name is required")
        if "@" not in self._data.get("email", ""):
            raise ValueError("Valid email is required")
        if self._data.get("salary", 0) < 0:
            raise ValueError("Salary cannot be negative")
        for field in ("department", "position", "salary"):
            if field not in self._data:
                raise ValueError(f"{field} is required")
        return Employee(**self._data)


class DeveloperBuilder(EmployeeBuilder):
    """Preset: a developer always gets a laptop + vpn + admin rights"""

    def __init__(self, first_name, last_name, email, salary=60000):
        super().__init__()
        (self.with_name(first_name, last_name)
             .with_email(email)
             .with_job("Engineering", "Developer", salary)
             .with_equipment(laptop=True)
             .with_access(vpn=True, admin=True)
             .in_office("Paris HQ"))


class InternBuilder(EmployeeBuilder):
    def __init__(self, first_name, last_name, email, department):
        super().__init__()
        (self.with_name(first_name, last_name)
             .with_email(email)
             .with_job(department, "Intern", 15000)
             .with_equipment(laptop=True)
             .with_contract("internship")
             .in_office("Paris HQ"))


if __name__ == "__main__":
    employee = (
        EmployeeBuilder()
        .with_name("John", "Doe")
        .with_email("john.doe@company.com")
        .with_job("Engineering", "Senior Developer", 75000)
        .with_equipment(laptop=True, parking=False)
        .with_access(vpn=True, admin=True)
        .build()
    )
    print(employee)

    dev = DeveloperBuilder("John", "Doe", "john.doe@company.com").build()
    intern = InternBuilder("Jane", "Smith", "jane.smith@company.com", "Marketing").with_manager(42).build()
    print(dev)
    print(intern)
