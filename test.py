from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()
print(os.getenv("INSTRUCTION"))
print(os.getenv('GEMINI_API_KEY'))

