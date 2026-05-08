from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

class Patient(BaseModel):

    id: Annotated[str, Field(..., description="The ID of the patient", examples=['P001'])]

    name: Annotated[str, Field(..., description="The name of the patient")]

    city:Annotated[str, Field(..., description="The city where the patient lives")]

    age: Annotated[int, Field(..., gt=0, lt=120, description="The age of the patient")]

    gender:Annotated[Literal['male', 'female', 'other'], Field(..., description="The gender of the patient")]

    height:Annotated[float, Field(..., gt=0, description="The height of the patient")]

    weight:Annotated[float, Field(..., gt=0, description="The weight of the patient")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = self.weight / (self.height/100) ** 2
        return round(bmi, 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'underweight'
        elif 18.5 <= self.bmi < 25:
            return 'normal weight'
        elif 25 <= self.bmi < 30:
            return 'overweight'
        else:
            return 'obese'
        
class Patient_update(BaseModel):

    name: Annotated[Optional[str], Field(default=None)]
    city:Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender:Annotated[Optional[Literal['male', 'female', 'other']], Field(default=None)]
    height:Annotated[Optional[float], Field(default=None, gt=0)]
    weight:Annotated[Optional[float], Field(default=None, gt=0)]


app = FastAPI()

def load_data():
    # Code to load data from a file or database
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    # Code to save data to a file or database
    with open('patients.json', 'w') as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return {"message": "patient management system api"}

@app.get('/about')
def about():
    return{'message':'a fully functional api to manage patients and their medical records'}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", examples='P001')):
    #load all the patients
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description="sort on the basis of height weight or bmi"), order:str = Query('asc', description='sort in asc or desc order')):

    valid_fielsds = ['height', 'weight', 'bmi']

    if sort_by not in valid_fielsds:
        raise HTTPException(status_code=400, detail=f'Invalid sort field select from {valid_fielsds}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order select from 'asc' or 'desc'")
    
    data = load_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by,0), reverse=sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):

    #load the existing data
    data = load_data()

    #check if the patient with the same id already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    
    #insert the new patient data
    data[patient.id] = patient.model_dump(exclude=['id'])

    #save the updated data
    save_data(data)

    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: Patient_update):
    #load the existing data
    data = load_data()

    #check if the patient with the given id exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    #updating bmi and verdict
    existing_patient_info['id'] = patient_id
    patient_pydantic_object = Patient(**existing_patient_info)
    existing_patient_info = patient_pydantic_object.model_dump(exclude='id')

    #add this dict to data
    data[patient_id] = existing_patient_info

    #save the updated data
    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    #load the existing data
    data = load_data()

    #check if the patient with the given id exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    #delete the patient data
    del data[patient_id]

    #save the updated data
    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"})