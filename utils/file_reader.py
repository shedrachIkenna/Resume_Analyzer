import os
import fitz  # PyMuPDF

def read_txt(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def read_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def read_resume_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.txt':
        return read_txt(file_path)
    elif ext == '.pdf':
        return read_pdf(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
