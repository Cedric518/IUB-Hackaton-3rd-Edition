import os
from dotenv import load_dotenv
import google.generativeai as genai
from DatabaseManager import DatabaseManager
from geminichat import ChatModel

load_dotenv()

INSTRUCTION = os.getenv("INSTRUCTION")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DATABASE_NAME = os.getenv('DATABASE_NAME')
CHATBOT_VERSION = os.getenv('CHATBOT_VERSION')


chat_bot = ChatModel(CHATBOT_VERSION, GEMINI_API_KEY, INSTRUCTION)

print(f"THIS IS THE INSTRUCTION: {INSTRUCTION}")

def test(query, parameters):
    print(f"THIS IS QUERY: {query}")
    print(f"PARAMETERS: {parameters}")

manager = DatabaseManager(DATABASE_NAME)

def get_valid_input():
    while True:
        user_input = chat_bot.start_chat()
        if not user_input or "\n" in user_input or "\t" in user_input:
            print(user_input +" is what you said. Please try again.")
        else:
            print(f"THIS IS THE USER_INPUT: {user_input}")
            return user_input

while True:
    user_input = get_valid_input()
    model_response = chat_bot.send_message(user_input)
    
    if not ('sql' in model_response and 'parameters' in model_response 
            and 'action' in model_response and 'value' in model_response):
        print("Invalid response format. Please try again.")
        continue
    elif user_input.strip().upper() != "CLOSE" and (model_response['sql'] == 'None' or model_response['parameters'] == '[]' or model_response['action'] == 'None' or model_response['value'] == 'None'):
        print("Invalid response format. Please try again.")
        continue    
    
    print(f"THIS IS THE MODEL_RESPONSE: {model_response}")
    query = model_response['sql']
    parameters = model_response['parameters']
    action = model_response['action']
    value = model_response['value']

    try:
        if action == 'INSERT':
            result = manager.push_data(query, parameters)
        elif action == 'UPDATE':
            result = manager.update_data(query, parameters)
        elif action == 'SELECT':
            result = manager.select_data(query, parameters)
        elif action == 'DELETE':
            result = manager.delete_data(query, parameters)
        elif action == 'DELETE_ALL':
            duo_validation = input('Confirm to delete the full database (Y/N)? ').strip().upper()
            if duo_validation in ['Y', 'YES']:
                manager.delete_all(query)
            else:
                print("Deletion aborted.")
        elif action == 'CLOSE':
            print("Closing database connection...")
            break
        else:
            print("Unknown action. Please try again.")
            continue

        if action != 'CLOSE':
            test(query, parameters)
            manager.show_data()

    except Exception as e:
        print(f"Error executing action: {e}")
        user_input = ""

manager.close()


        


'''
THIS IS THE MODEL_RESPONSE: {'sql': 'INSERT INTO key_value_store (key, value, created_datetime, updated_datetime) VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)', 
                            'parameters': ['user.email', 'cedrchen@gmail.comos'], 
                            'action': 'INSERT', 
                            'value': 'cedrchen@gmail.comos'}

                            
Single record inserted: ['user.email', 'cedrchen@gmail.comos']


WHAT SHOULD I DO TMR:
- retrive action
- show all data
'''