import spacy 

SKILLS_KEYWORD = {
    "python", "sql", "machine learning", "deep learning", "pandas", "flask",
    "react", "docker", "aws", "tensorflow", "nlp", "excel", "git", "fastapi"
}

nlp = spacy.load("en_core_web_sm")

def extract_skills(text: str) -> str:
    doc = nlp(text.lower())
    extracted = set()

    for token in doc:
        if token.text in SKILLS_KEYWORD:
            extracted.add(token.text)

    return list(extracted)