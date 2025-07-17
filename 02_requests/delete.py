from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

## Utility Functions
# fetch data
def load_data():
    with open('../patients.json', 'r') as f:
        data = json.load(f)
        
    return data

# save updated data
def save_data(data):
    with open('../patients.json', 'w') as f:
        json.dump(data, f)
    

# Pydantic Model
class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Patient ID", examples=['P001'])] # ... -> indicates that field is required property
    name: Annotated[str, Field(..., description="Patient's Full Name")]
    city: Annotated[str, Field(..., description="city from which patient belongs to")]
    age: Annotated[int, Field(..., description="Patient's Age", gt=0, lt=120)]
    gender: Annotated[Literal['Male', 'Female', 'Other'], Field(..., description="Patient's Gender")]
    height: Annotated[float, Field(..., description="Patient's Height (in mtrs)", gt=0)]
    weight: Annotated[float, Field(..., description="Patient's Weight (in kgs)", gt=0)]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5: 
            return "Underweight"
        elif self.bmi >= 18.5 and self.bmi < 25: 
            return "Normal" 
        elif self.bmi >= 25 and self.bmi < 30: 
            return "Overweight"
        else: 
            return "Obese"
        
## Pydantic Model to Update the Original Schema
class UpdatePatient(BaseModel):
    name: Annotated[Optional[str], Field(..., description="Patient's Full Name")]
    city: Annotated[Optional[str], Field(..., description="city from which patient belongs to")]
    age: Annotated[Optional[int], Field(..., description="Patient's Age", gt=0, lt=120)]
    gender: Annotated[Optional[Literal['Male', 'Female', 'Other']], Field(..., description="Patient's Gender")]
    height: Annotated[Optional[float], Field(..., description="Patient's Height (in mtrs)", gt=0)]
    weight: Annotated[Optional[float], Field(..., description="Patient's Weight (in kgs)", gt=0)]
    
    
    
    
    
@app.put('/edit/{patient_id}')
def update_patient_details(patient_id: str, updated_details: UpdatePatient):
    data = load_data()
    
    # check if patients exist or not
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="patient not found")
    
    existing_patient_details = data[patient_id]
    # converting UpdatePatient object to dict
    updated_details = updated_details.model_dump(exclude_unset=True) # dict will only contain keys with value present in it
    # updating the details
    for key, value in updated_details.items():
        existing_patient_details[key] = value # only newly provided details will be updated
        
    # what if weight / height value get changed, it'll affect bmi and verdict
    # existing_patient_details -> pydantic object (Patient) -> updated bmi + verdict
    existing_patient_details['id'] = patient_id
    updated_patient_pydantic_object = Patient(**existing_patient_details)
    # convert Patient's object to dict
    updated_patient_pydantic_object.model_dump(exclude='id')
        
    # updating details in DB
    data[patient_id] = existing_patient_details
    
    # save data
    save_data(data)
    
    return JSONResponse(
        status_code=200,
        content= "patient details updated"
    )
    
    
    
@app.delete('/delete/{patient_id}')
def delete_patient_details(patient_id: str):
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    del data[patient_id]
    
    save_data(data)
    
    return JSONResponse(
        status_code=200,
        content="patient details deleted"
    )