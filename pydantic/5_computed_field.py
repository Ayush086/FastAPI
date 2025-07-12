from pydantic import BaseModel, EmailStr, computed_field
from typing import List, Dict

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    height: float
    allergies: List[str]
    contact_details: Dict[str, str]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi
    
    
def insert_patient_data(patient: Patient):
    print(patient.name, " ", patient.age)
    print("bmi: ", patient.bmi)
    print('entry inserted')
    
    
patient_details = {'name': 'ayush', 'email': 'xyz@icici.com', 'age': 64,'weight': 64.0, 'height': 1.20, 'allergies': ['pollen', 'duest'], 'contact_details': {'emergency': '00000000000'}}
p1 = Patient(**patient_details)

insert_patient_data(p1)