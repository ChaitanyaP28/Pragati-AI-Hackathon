import os
import pdfplumber
from dotenv import load_dotenv
import google.generativeai as genai


import logging
logging.getLogger("pdfminer").setLevel(logging.ERROR)

# Load .env for Google API key and model name
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "models/gemini-1.5-pro")

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_skills_with_gemini(resume_text):
    prompt = (
        "You are an AI resume analyzer. From the following resume text, extract a list of technical and soft skills.\n\n"
        f"Resume Text:\n{resume_text}\n\n"
        "Return the skills in a bullet-point list format."
    )
    response = model.generate_content(prompt)
    return response.text.strip()

if __name__ == "__main__":
    pdf_path = input("Enter path to the resume PDF: ")
    resume_text = extract_text_from_pdf(pdf_path)
    #print("EXTRACTED TEXT:")
    #print(resume_text)
    #print()
    if not resume_text:
        print("⚠️ Could not extract text from the PDF.")
    else:
        skills = extract_skills_with_gemini(resume_text)
        print("\nExtracted Skills using AI:\n")
        print(skills)
