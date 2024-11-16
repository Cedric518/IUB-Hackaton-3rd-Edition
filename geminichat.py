import os
from dotenv import load_dotenv
import google.generativeai as genai
from sql import SQL
import json
# -m venv venv
# .\venv\Scripts\activate
# pip install google-generativeai



class ChatModel:

    def __init__(self, model_name, api_key, instruction):
        self.genai = genai
        self.genai.configure(api_key=api_key)
        generation_config = {
            "temperature": 0,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        }

        self.model = self.genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            system_instruction=instruction
        )

        self.history = []
        self.chat_session = None

    def start_chat(self):
        print('Hello, this is your personalized database manager, how can I help you')

        user_input = input('You: ') #system request input from user

        self.chat_session = self.model.start_chat(history=self.history)

        return user_input

    def send_message(self, user_input):
        response = self.chat_session.send_message(user_input)
        self._update_history(user_input, response.text)
        return self.convert(response.text)
    
    def _update_history(self, user_input, model_response):
        self.history.append({'role': 'user', 'parts': [user_input]})
        self.history.append({'role': 'model', 'parts': [model_response]})

    def convert(self, msg):
        return json.loads(msg)



# Create the model



# create a model instance and save into variable model

# You are a personal assistant that manage a database. Your role is to interpret natural language commands and convert them into database operations (INSERT, UPDATE, DELETE, GET).

# while True:

#     user_input = input('You: ') #system request input from user -> line33

#     chat_session = model.start_chat(
#         history=history
#     )

#     response = chat_session.send_message(user_input) #input get pass into gemini api
#     model_response = response.text
    
#     print(model_response)

#     #make a instance of SQL class 
#     model_response = SQL(model_response['sql'], model_response['parameters'])

#     # put conversation into history 
#     history.append({'role': 'user', 'parts': [user_input]})
#     history.append({'role': 'model', 'parts': [model_response]})


'''
response (object):
GenerateContentResponse(
    done=True,
    iterator=None,
    result=protos.GenerateContentResponse({
        "candidates": [
            {
            "content": {
                "parts": [
                {
                    "text": "{\"response\": \"I can process database operations such as INSERT, UPDATE, DELETE, and GET based on your natural language instructions. Please tell me what you would like to do.\"}\n\n"
                }
                ],
                "role": "model"
            },
            "finish_reason": "STOP",
            "avg_logprobs": -0.1656598166415566
            }
        ],
        "usage_metadata": {
            "prompt_token_count": 43,
            "candidates_token_count": 38,
            "total_token_count": 81
        }
    }),
)
'''