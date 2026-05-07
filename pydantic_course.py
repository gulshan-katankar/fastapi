from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str = Annotated[str. Field(min_length=2, max_length=50, description="Name must be between 2 and 50 characters",examples = ['nitish', 'ghollu'])]
    email: EmailStr
    linekedin: Optional[AnyUrl] = None
    age: int
    weight :float = Field(..., gt=0, description="Weight must be greater than zero")
    married: Optional[bool] = None
    allergies: list[str]
    contact_details: Dict[str, str]

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print('inserted')

patient_info = {'name': 'gulshan', 'age': 40, 'weight': 70.5, 'married': True, 'allergies': ['pollen', 'dust'], 'contact_details': {'email': 'gulshan@example.com'}}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)