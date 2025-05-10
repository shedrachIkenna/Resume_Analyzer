from utils.file_reader import read_resume_text
from nlp.skill_extractor import extract_skills

def main():
    file_path = 'resume/sample_resume.txt'
    resume_text = read_resume_text(file_path)
    print(f"\n===== Resume Content =====")
    print(resume_text)

    print(f"\n===== Extracted Skills =====")
    skills = extract_skills(resume_text)
    print(skills)


if __name__ == "__main__":
    main()