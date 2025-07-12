from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as file:
        data = json.load(file)
    
    return data

@app.get('/')
def read_root():
    return {'message': 'Patient Management System API'}

@app.get('/about')
def about():
    return {
        'message': 'This is a Patient Management System API',
        'version': '1.0.0'
    }
    
@app.get('/view')
def view_patients():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient_details(patient_id: str = Path(..., description="Patient ID to search for", example="P001")):
    # load patients data
    data = load_data()
    
    # perform searching
    if patient_id in data:
        return data[patient_id]
    
    # if patient not found
    raise HTTPException(status_code=404, detail="Patient not found")


## Query Parameter
@app.get('/sorted-results')
def sorted_results(sort_by: str = Query(..., description="Sort by field", example="age"), order: str = Query('asc', description="Order of sorting", example="asc")):
    # validate query parameters
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Valid fields are: {', '.join(valid_fields)}")
    
    if order not in ['asc', 'dsc']:
        raise HTTPException(status_code=400, detail=f'Invalid order. Valid orders: asc/desc')
    
    # load data
    data = load_data()
    
    # sort based on height
    sort_order = True if order == 'desc' else False
    data_vals = data.values()
    sorted_data = sorted(data_vals, key = lambda x: x.get(sort_by, 0), reverse=sort_order)
    
    return sorted_data



    