from dataclasses import dataclass
from typing import List

@dataclass
class Person:
    f_name: str
    l_name: str
    age: int

    def full_name(self) -> str:
        return(self.f_name + ' ' + self.l_name)

@dataclass
class Employee(Person): # inheritance
    emp_id: int = 0
    dept: str = 'Unknown'

    # Equality depends on the employee id only
    def __eq__(self, other):
        return self.emp_id == other.emp_id

@dataclass
class Company:
    name: str
    employees: List[Employee]