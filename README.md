# Insurance Premium/Risk Prediction API

A FastAPI backend serving a machine learning model to predict insurance premium categories or risk levels based on user inputs, with a simple HTML/JS frontend for demonstration.

## Features
- FastAPI backend with Pydantic data validation
- Pre-trained ML model integration (`model.pkl`)
- CORS enabled for frontend access
- Basic HTML/CSS/JS frontend for testing

## Tech Stack
- Python, FastAPI, Pydantic, Pandas
- Scikit-learn (assumed for model)
- Uvicorn (ASGI server)
- HTML/CSS/JavaScript frontend




## Setup

1. Clone the repo:

git clone https://github.com/Prince-Bhattrai/insurance-ml-api.git
cd your-repo-name
Create and activate a virtual environment:


# Windows
python -m venv venv

venv\Scripts\activate
# macOS/Linux
python -m venv venv

source venv/bin/activate
Install dependencies:


pip install fastapi uvicorn pandas scikit-learn
Add your trained model as model.pkl in the root directory.

Running
Start the backend:


uvicorn main:app --reload
Open index.html in a browser for the frontend.

API docs: http://127.0.0.1:8000/docs

Usage
Frontend
Fill form fields (age, weight, height, income, smoker status, city, occupation) and click "Predict".

API
POST to /predict with JSON:

json

{
  "age": 30,
  "weight": 70.5,
  "height": 1.75,
  "income_lpa": 12.5,
  "smoker": false,
  "city": "Hyderabad",
  "occupation": "private_job"
}
Response example:


{
  "predicted_category": "Low Risk"
}
Notes
model.pkl is required.

Robust input validation is implemented.

CORS allows all origins for development; restrict in production.
