from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

# pydantic schema (class)
class Patient(BaseModel):
    # type validation + custom data validation
    name: Annotated[str, Field(max_length=500, title='Patient Name', description='Full name of the patient should be provided', examples=['Yuvraj', 'Nishith'])]
    email: EmailStr
    social_profile: AnyUrl
    age: int = Field(ge=0, strict=True) # it'll only consider int values. even if i provide '22' it'll throw validation error
    is_married: Annotated[bool, Field(default=None, description='is patient married or not')]
    allergies: Optional[List[str]] = None # marking this field as optional (it's compulsory to define optional value with a default value)
    contact_details: Dict[str, str]
    
# """might be thinking that why didn't we used list/dict for validation ? it's because we want to validate the data type of container as well as the values inside the container. In our case inside list string values must be present no any other values. Same goes for dictionary datatype. """

    
    
    

def insert_patient_data(patient: Patient):
    print(patient.name, " ", patient.age)
    print('entry inserted')
    

patient_details = {'name': 'ayush', 'email': 'xyz@gmail.com', 'social_profile': 'https://github.com/Ayush086', 'age': 22, 'allergies': ['pollen', 'duest'], 'contact_details': {'phone': '00000000000'}}
p1 = Patient(**patient_details)

insert_patient_data(p1)