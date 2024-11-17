from dotenv import load_dotenv
import google.generativeai as genai
from geminichat import ChatModel
import os
import pprint

load_dotenv()

INSTRUCTION = os.getenv("INSTRUCTION")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DATABASE_NAME = os.getenv('DATABASE_NAME')
CHATBOT_VERSION = os.getenv('CHATBOT_VERSION')


chat_bot = ChatModel(CHATBOT_VERSION, GEMINI_API_KEY, INSTRUCTION)

class Test:
    def __init__(self, prompt, expected):
        self.prompt = prompt
        self.expected = expected
        chat_bot.test_start_chat(prompt)
        model_response = chat_bot.send_message(prompt)
        self.actual = pprint.pformat(model_response)

    def __str__(self):
        
        #return self.prompt == self.expected
        return f"User:{self.actual} \n Expected Answer:{self.expected}"



class TestRunner:
    # Test that prompting works
    t1 = Test("Add Value 8487684148 to Key phone numbers", "{'action': 'INSERT',\n'parameters': ['phone numbers', '8487684148'],\n'sql': 'INSERT INTO key_value_store (key, value, created_datetime, '\n    'updated_datetime) VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)',\n'value': '8487684148'}")
    print(t1.__str__()) # same
    # Tests for filtering of prompts
    t2 = Test("\n", "") #throw errors
    t3 = Test("\t", "") #throw errors
    t4 = Test("", "") #throw errors
    print(t2.__str__()) 
    print(t2.__str__()) 
    print(t2.__str__())  
    

