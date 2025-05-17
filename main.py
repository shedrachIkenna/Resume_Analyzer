from utils.file_reader import read_resume_text
from nlp.skill_extractor import extract_skills

def main():
    file_path = r'C:\Users\DELL\Desktop\smart_resume_analyser\resume\sample_resume.txt'
    resume_text = read_resume_text(file_path)

    print("\n===== Resume Content =====\n")
    print(resume_text)

    print("\n===== Extracted Skills =====\n")
    skills = extract_skills(resume_text)
    print(skills)

if __name__ == '__main__':
    main()
