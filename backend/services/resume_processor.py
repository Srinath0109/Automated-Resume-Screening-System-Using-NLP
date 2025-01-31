import spacy
import pdfplumber
import re
from nltk.tokenize import word_tokenize
from collections import Counter

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_file):
    """Extract text from a given PDF file."""
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def clean_text(text):
    """Preprocess text (lowercase, remove special chars)."""
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text.lower())
    return text

def calculate_match_score(resume_text, job_description):
    """Match keywords from job description with resume."""
    job_tokens = word_tokenize(clean_text(job_description))
    resume_tokens = word_tokenize(clean_text(resume_text))
    
    job_counter = Counter(job_tokens)
    resume_counter = Counter(resume_tokens)
    
    match_score = sum(min(job_counter[word], resume_counter[word]) for word in job_counter)
    
    return match_score / len(job_tokens) * 100  # Percentage match

def process_resume(file, job_desc):
    """Process resume and return match score."""
    resume_text = extract_text_from_pdf(file)
    score = calculate_match_score(resume_text, job_desc)
    return round(score, 2)
