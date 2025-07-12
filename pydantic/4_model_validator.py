from pydantic import BaseModel, EmailStr, model_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    is_married: bool
    allergies: List[str]
    contact_details: Dict[str, str]
    
    @model_validator(mode='after')
    @classmethod
    def add_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError("emergency contact needed")
        return model
    
    
def insert_patient_data(patient: Patient):
    print(patient.name, " ", patient.age)
    print('entry inserted')
    
    
patient_details = {'name': 'ayush', 'email': 'xyz@icici.com', 'age': 64, 'is_married': False, 'allergies': ['pollen', 'duest'], 'contact_details': {'emergency': '00000000000'}}
p1 = Patient(**patient_details)

insert_patient_data(p1)