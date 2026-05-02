from fastapi import FastAPI
import json

app = FastAPI()

def load_data():
    # Code to load data from a file or database
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

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