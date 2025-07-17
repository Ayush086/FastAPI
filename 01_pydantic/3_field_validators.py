from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    is_married: bool
    allergies: List[str]
    contact_details: Dict[str, str]
    
    @field_validator('email')
    @classmethod
    def check_employee(cls, value):
        valid_domains = ['hdfc.com', 'icici.com']
        # eg. xyz@hdfc.com
        domain_name = value.split('@')[-1]
        
        if domain_name not in valid_domains:
            raise ValueError("Not a valid employee") 
        
        return value
    
    @field_validator('name')
    @classmethod
    def capitalize_name(cls, value):
        return value.upper()
    
    @field_validator('age', mode='before')
    @classmethod
    def validate_age(cls, value):
        if 0 <= value < 120:
            return value
        else: 
            raise ValueError('age value is invalid')
    
def insert_patient_data(patient: Patient):
    print(patient.name, " ", patient.age)
    print('entry inserted')
    
    
patient_details = {'name': 'ayush', 'email': 'xyz@icici.com', 'age': 22, 'is_married': False, 'allergies': ['pollen', 'duest'], 'contact_details': {'phone': '00000000000'}}
p1 = Patient(**patient_details)

insert_patient_data(p1)