import fitz  
import io
from PyPDF2 import PdfReader
import re
import pdfplumber
from docx import Document

def extract_text(file_bytes, filename):
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    else:
        return "Unsupported file format"

def extract_text_from_pdf(file_bytes):
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file_bytes):
    text = ""
    doc = Document(io.BytesIO(file_bytes))
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

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

