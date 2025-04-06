import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "models/gemini-1.5-pro")  # fallback if not set

#print("Using model:", MODEL_NAME)
# Configure Gemini
genai.configure(api_key=API_KEY)

# Initialize model
model = genai.GenerativeModel(MODEL_NAME)

def generate_mcq_questions(topic):
    prompt = (
        f"Generate 10 multiple-choice questions (MCQs) on the topic: '{topic}'.\n"
        "Each question should have:\n"
        "- A clear question statement\n"
        "- Exactly 4 answer options (A, B, C, D)\n"
        "- Mark the correct option with an asterisk (*) at the end of the correct answer.\n\n"
        "Format:\n"
        "Q1. Question text?\n"
        "A. Option 1\n"
        "B. Option 2\n"
        "C. Option 3\n"
        "D. Option 4*\n"
        "\nRepeat similarly for Q2 to Q10."
    )

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    user_topic = input("Enter a topic: ")
    questions = generate_mcq_questions(user_topic)
    print("\nGenerated MCQs:\n")
    print(questions)
