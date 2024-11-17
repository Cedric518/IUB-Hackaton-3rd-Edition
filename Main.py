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

while True:
    user_input = chat_bot.start_chat()
    model_response = chat_bot.send_message(user_input)
    print(f"THIS IS THE MODEL_RESPONSE: {model_response}")

    query = model_response['sql']
    parameters = model_response['parameters']
    action = model_response['action']
    value = model_response['value']

    # print(f"THIS IS PARAMETER: {parameters}")
    # print(f"THIS IS QUERY: {query}")
    # print(f"THIS IS ACTION: {action}")
    # print(f"THIS IS VALUE: {value}")
    manager = DatabaseManager(DATABASE_NAME)
    
    try:
        if action == 'INSERT':
            result = manager.push_data(query, parameters)
            test(query, parameters)
            manager.show_data()
        
        elif action == 'UPDATE':
            result = manager.update_data(query, parameters)
            test(query, parameters)
            manager.show_data()

        elif action == 'SELECT':
            result = manager.select_data(query, parameters)
            test(query, parameters)
            manager.show_data()

        elif action == 'DELETE':
            result = manager.delete_data(query, parameters)
            test(query, parameters)
            manager.show_data()

        elif action == 'DELETE_ALL':
            duo_validation = input('Confirm to delete the full database (Y/N)?').upper()
            if duo_validation == 'Y' or duo_validation == 'YES':
                manager.delete_all(query)
        
        elif action == 'CLOSE':
            print('Closing database connection...')
            manager.close()

    except Exception as e:
        print(f"Error excuting action {e}")
    
    finally:
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