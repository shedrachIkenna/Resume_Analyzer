import spacy 
import PyPDF2 

nlp = spacy.load("en_core_web_sm")

SKILLS_KEYWORD = {
    "python", "sql", "machine learning", 
    "deep learning", "pandas", "flask",
    "react", "docker", "aws", "tensorflow", 
    "nlp", "excel", "git", "fastapi"
}


def file_reader(file_path):
    # Check if the file is a PDF
    if file_path.lower().endswith('.pdf'):
        
        # Open PDF in binary mode
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text = ""
            # Extract text from each page
            for page in pdf_reader.pages:
                text += page.extract_text() or ""  # Handle None return
            return text
    else:
        # For text files
        with open(file_path, 'r', encoding="utf-8") as f:
            return f.read()


def extract_skill(text: str) -> str:
    doc = nlp(text.lower())
    extracted = set()

    for token in doc:
        if token.text in SKILLS_KEYWORD:
            extracted.add(token.text)

    return list(extracted)

def main():
    file_path = r'C:\Users\DELL\Desktop\CV\CV.pdf'
    resume_text = file_reader(file_path)
    print("\n ===== Resume Content =====")
    print(resume_text)

    print("\n ===== Extracted Skills =====")
    skills = extract_skill(resume_text)
    print(skills)


if __name__ == "__main__":
    main()