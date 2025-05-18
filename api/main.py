from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from resume_parser.extractor import extract_text
from nlp.info_extractor import extract_email, extract_phone, extract_name, extract_education
from nlp.skill_extractor import extract_skills
from ml.model import predict_roles
from utils.report_generator import generate_pdf_report

from api.auth import router as auth_router
from api.auth import get_current_user

app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Your Vite frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route
@app.get("/")
def root():
    return {"message": "Welcome to Smart Resume Analyser API!"}

# ✅ Authenticated prediction route
@app.post("/predict")
async def predict_resume(file: UploadFile = File(...), user: dict = Depends(get_current_user)):
    contents = await file.read()
    text = extract_text(contents, file.filename)

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "education": extract_education(text),
        "skills": extract_skills(text),
        "predicted_roles": predict_roles(text)
    }

# ✅ Authenticated download route
@app.post("/download")
async def download_report(file: UploadFile = File(...), user: dict = Depends(get_current_user)):
    contents = await file.read()
    text = extract_text(contents, file.filename)

    data = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "education": extract_education(text),
        "skills": extract_skills(text),
        "predicted_roles": predict_roles(text)
    }

    pdf_path = generate_pdf_report(data)
    return FileResponse(pdf_path, media_type='application/pdf', filename="resume_report.pdf")

# ✅ Auth routes
app.include_router(auth_router)
