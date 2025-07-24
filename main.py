# from fastapi import FastAPI
# from pydantic import BaseModel, Field, computed_field
# from typing import Annotated
# import pickle
# import pandas as pd
# from fastapi.responses import JSONResponse

# with open("model.pkl", "rb") as f:
#     model = pickle.load(f)

# app = FastAPI()

# class userInput(BaseModel):
#     age: Annotated[int, Field(..., gt=0, lt=120)]
#     weight: Annotated[float, Field(..., gt=0)]
#     height: Annotated[float, Field(..., gt=0)]
#     income_lpa: Annotated[int, Field(...)]
#     smoker: Annotated[bool, Field(...)]
#     city: Annotated[str, Field(...)]
#     occupation: Annotated[str, Field(...)]

#     @computed_field
#     @property
#     def bmi(self) -> float:
#         return self.weight / (self.height ** 2)

#     @computed_field
#     @property
#     def lifestyle_risk(self) -> str:
#         if self.smoker and self.bmi > 30:
#             return "high"
#         elif self.smoker or self.bmi > 27:
#             return "medium"
#         else:
#             return "low"

#     @computed_field
#     @property
#     def city_tier(self) -> int:
#         if self.city.lower() == "kathmandu":
#             return 1
#         elif self.city.lower() == "nepalgunj":
#             return 2
#         else:
#             return 3

# @app.get("/")
# def home():
#     return JSONResponse(status_code=200, content={"success": True, "message": "This is homepage"})

# @app.post("/predict")
# def predict_premium(data: userInput):
#     input_df = pd.DataFrame([{
#         "bmi": data.bmi,
#         "age": data.age,
#         "lifestyle_risk": data.lifestyle_risk,
#         "city_tier": data.city_tier,
#         "income_lpa": data.income_lpa,
#         "occupation": data.occupation
#     }])
#     prediction = model.predict(input_df)[0]
#     return JSONResponse(status_code=200, content={"prediction": prediction})



# from fastapi import FastAPI
# from pydantic import BaseModel, Field
# from typing import Annotated
# import pickle
# import pandas as pd
# from fastapi.responses import JSONResponse

# with open("model.pkl", "rb") as f:
#     model = pickle.load(f)

# app = FastAPI()

# class userInput(BaseModel):
#     age: Annotated[int, Field(..., gt=0, lt=120)]
#     weight: Annotated[float, Field(..., gt=0)]
#     height: Annotated[float, Field(..., gt=0)]
#     income_lpa: Annotated[int, Field(...)]
#     smoker: Annotated[bool, Field(...)]
#     city: Annotated[str, Field(...)]
#     occupation: Annotated[str, Field(...)]

#     @property
#     def bmi(self) -> float:
#         return self.weight / (self.height ** 2)

#     @property
#     def lifestyle_risk(self) -> str:
#         if self.smoker and self.bmi > 30:
#             return "high"
#         elif self.smoker or self.bmi > 27:
#             return "medium"
#         else:
#             return "low"

#     @property
#     def city_tier(self) -> int:
#         if self.city.lower() == "kathmandu":
#             return 1
#         elif self.city.lower() == "nepalgunj":
#             return 2
#         else:
#             return 3

# @app.get("/")
# def home():
#     return JSONResponse(status_code=200, content={"success": True, "message": "This is homepage"})

# @app.post("/predict")
# def predict_premium(data: userInput):
#     input_df = pd.DataFrame([{
#         "bmi": data.bmi,
#         "age": data.age,
#         "lifestyle_risk": data.lifestyle_risk,
#         "city_tier": data.city_tier,
#         "income_lpa": data.income_lpa,
#         "occupation": data.occupation
#     }])
#     prediction = model.predict(input_df)[0]
#     return JSONResponse(status_code=200, content={"prediction": prediction})



from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware



# import the ml model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

app = FastAPI()

app.add_middleware(
    
    CORSMiddleware,
    allow_origins=["*"],  # or specify frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

# pydantic model to validate incoming data
class UserInput(BaseModel):

    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the user')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the user')]
    height: Annotated[float, Field(..., gt=0, lt=2.5, description='Height of the user')]
    income_lpa: Annotated[float, Field(..., gt=0, description='Annual salary of the user in lpa')]
    smoker: Annotated[bool, Field(..., description='Is user a smoker')]
    city: Annotated[str, Field(..., description='The city that the user belongs to')]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(..., description='Occupation of the user')]
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3

@app.post('/predict')
def predict_premium(data: UserInput):

    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }])

    prediction =  model.predict(input_df)[0]

    return JSONResponse(status_code=200, content={'predicted_category': prediction})




