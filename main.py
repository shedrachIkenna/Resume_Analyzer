from utils.file_reader import read_resume_text
from nlp.skill_extractor import extract_skills
from nlp.info_extractor import extract_email, extract_phone, extract_name, extract_education
import joblib

def main():
    file_path = r'C:\Users\DELL\Desktop\smart_resume_analyser\resume\sample_resume.txt'
    resume_text = read_resume_text(file_path)

    print("\n===== Resume Content =====\n")
    print(resume_text)

    print("\n===== Extracted Skills =====\n")
    skills = extract_skills(resume_text)
    print(skills)

    print("\n ===== Candidate Info =====")
    print("\n===== Resume Information =====\n")
    print("Name:", extract_name(resume_text))
    print("Email:", extract_email(resume_text))
    print("Phone:", extract_phone(resume_text))
    print("Education:", extract_education(resume_text))

    print("\n===== Predicted Job Role(s) =====\n")
    roles = predict_roles(resume_text)
    print(roles)


def predict_roles(resume_text: str):
    model = joblib.load('ml/model.joblib')
    mlb = joblib.load('ml/label_binarizer.joblib')
    pred = model.predict([resume_text])
    labels = mlb.inverse_transform(pred)
    return labels[0]

if __name__ == '__main__':
    main()
