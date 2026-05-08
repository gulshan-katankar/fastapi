from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle
import pandas as pd

#import the model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]

tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"]

#pydantic model for input data validation
class user_input(BaseModel):

    age: Annotated[int, Field(..., gt=0, lt=120, description="The age of the user")]

    weight:Annotated[float, Field(..., gt=0, description="The weight of the user")]

    height:Annotated[float, Field(..., gt=0, lt=2.5, description="The height of the user")]

    income_lpa:Annotated[float, Field(..., gt=0, description="The income of the user in lakhs per annum")]

    smoker: Annotated[bool, Field(..., description="Whether the user is a smoker or not")]

    city: Annotated[str, Field(..., description="The city where the user lives")]

    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job'],Field(..., description="The occupation of the user")]

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height ** 2)
    
    @computed_field
    @property   
    def lifestyle_risk(self)->str:
        if self.smoker and self.bmi > 30:
            return 'high'
        elif self.smoker or self.bmi>27:
            return 'medium'
        else:
            return 'low'
        
    @computed_field
    @property
    def age_group(self)->str:
        if self.age < 25:
            return 'young'
        elif self.age < 45:
            return 'adult'
        elif self.age < 60:
            return 'middle-aged'
        return 'senior'
    
    @computed_field
    @property   
    def city_tier(self)->int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
        
@app.post('/predict')
def predict_premium(data: user_input):

    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,    
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }])

    prediction = model.predict(input_df)[0]

    return JSONResponse (status_code=200, content={'predicted_category': prediction})