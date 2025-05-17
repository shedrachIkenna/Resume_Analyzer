import re

def extract_email(text: str):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None

def extract_phone(text: str):
    match = re.search(r'(\+?\d{1,3})?[\s.-]?(\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}', text)
    return match.group(0) if match else None

def extract_name(text: str):
    # For now, assume name is the first line of the resume
    lines = text.strip().split('\n')
    if lines:
        first_line = lines[0].strip()
        if len(first_line.split()) <= 4:  # crude assumption
            return first_line
    return None

def extract_education(text: str):
    education_keywords = ['bachelor', 'b.sc', 'bsc', 'master', 'msc', 'phd', 'degree', 'university', 'college']
    education_lines = []
    for line in text.split('\n'):
        for keyword in education_keywords:
            if keyword in line.lower():
                education_lines.append(line.strip())
                break
    return education_lines
