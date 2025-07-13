from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
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
        
        
    
@app.post('/create')
def add_patient(patient_details: Patient):
    #load existing data
    data = load_data()
    
    # check if new patient already exists
    if patient_details.id in data: 
        raise HTTPException(status_code=400, detail="Patients details already exists")
    
    # if not, then create new entry
    data[patient_details.id] = patient_details.model_dump(exclude=['id'])
    
    # save into json file
    save_data(data)
    
    # send success response
    return JSONResponse(status_code=201, content={'message': "new patient added successfully"})
    
    
    
    
    
    
    
