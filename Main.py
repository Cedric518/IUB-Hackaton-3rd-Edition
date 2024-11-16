import os
from dotenv import load_dotenv
import google.generativeai as genai
from sql import SQL
from geminichat import ChatModel

load_dotenv()

INSTRUCTION = os.getenv("INSTRUCTION")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DATABASE_NAME = os.getenv('DATABASE_NAME')


chat_bot = ChatModel("gemini-1.5-pro", GEMINI_API_KEY, INSTRUCTION)

while True:
    user_input = chat_bot.start_chat()
    model_response = chat_bot.send_message(user_input)

    data = SQL(model_response['sql'], model_response['parameters'])

    data.init_table(DATABASE_NAME)


