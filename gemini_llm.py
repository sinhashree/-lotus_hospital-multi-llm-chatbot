import google.generativeai as genai
import os

# Load API key from .env
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def ask_gemini(question, context):

    try:
        prompt = f"""
        You are a hospital assistant.

        Context:
        {context}

        Question:
        {question}
        """

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        print("Gemini Error:", e)
        return None