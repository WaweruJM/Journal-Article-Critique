import PyPDF2
import docx
import re
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        raise Exception(f"PDF extraction error: {str(e)}")
    return text

def extract_text_from_docx(docx_path):
    """Extract text from DOCX file"""
    text = ""
    try:
        doc = docx.Document(docx_path)
        for paragraph in doc.paragraphs:
            if paragraph.text:
                text += paragraph.text + "\n"
    except Exception as e:
        raise Exception(f"DOCX extraction error: {str(e)}")
    return text

def extract_text_from_file(file_path):
    """Extract text from either PDF or DOCX"""
    file_path = Path(file_path)
    if file_path.suffix.lower() == '.pdf':
        return extract_text_from_pdf(str(file_path))
    elif file_path.suffix.lower() == '.docx':
        return extract_text_from_docx(str(file_path))
    else:
        raise ValueError("Unsupported file type. Use PDF or DOCX.")

def clean_text(text):
    """Clean extracted text"""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove non-printable characters
    text = ''.join(char for char in text if char.isprintable() or char in '\n\t')
    return text.strip()