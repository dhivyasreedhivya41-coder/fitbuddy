import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

flash_model = genai.GenerativeModel("gemini-3.8-flash")


def generate_nutrition_tip_with_flash(goal: str) -> str:
    prompt = f"Give one clear, helpful nutrition or recovery tip for someone focused on '{goal}'. Keep it practical and friendly."
    try:
        response = flash_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating tip: {e}"