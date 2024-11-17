import os
from dotenv import load_dotenv
import google.generativeai as genai
from DatabaseManager import DatabaseManager
from geminichat import ChatModel

load_dotenv()

INSTRUCTION = os.getenv("INSTRUCTION")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DATABASE_NAME = os.getenv('DATABASE_NAME')


chat_bot = ChatModel("gemini-1.5-pro", GEMINI_API_KEY, INSTRUCTION)

while True:
    user_input = chat_bot.start_chat()
    model_response = chat_bot.send_message(user_input)

    manager = DatabaseManager(DATABASE_NAME)
    manager.push_data()