from fastapi import FastAPI, UploadFile, File
from resume_parser.extractor import extract_text
from nlp.info_extractor import extract_email, extract_phone, extract_name, extract_education
from nlp.skill_extractor import extract_skills
from ml.model import predict_roles
import joblib
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to Smart Resume Analyser API!"}

@app.post("/predict")
async def analyze_resume(file: UploadFile = File(...)):
    # Read file bytes
    contents = await file.read()
    
    # Extract text (works with .pdf for now)
    text = extract_text(contents, file.filename)

    # Extract fields
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    education = extract_education(text)
    skills = extract_skills(text)
    roles = predict_roles(text)

    # Optional score or summary can be added here later
    return {
        "name": name,
        "email": email,
        "phone": phone,
        "education": education,
        "skills": skills,
        "predicted_roles": roles
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

