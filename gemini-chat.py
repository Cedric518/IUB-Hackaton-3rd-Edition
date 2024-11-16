import os
from dotenv import load_dotenv
import google.generativeai as genai
# -m venv venv
# .\venv\Scripts\activate
# pip install google-generativeai

load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}
INSTRUCTION = os.getenv("INSTRUCTION")

# create a model instance and save into variable model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction=os.getenv("INSTRUCTION")
)
# You are a personal assistant that manage a database. Your role is to interpret natural language commands and convert them into database operations (INSERT, UPDATE, DELETE, GET).
history = []

print('Hello, this is your personalized database manager, how can I help you')

while True:

    user_input = input('You: ') #system request input from user -> line33

    chat_session = model.start_chat(
        history=history
    )

    response = chat_session.send_message(user_input) #input get pass into gemini api
    model_response = response.text
    
    print(model_response)
    

    # put conversation into history 
    history.append({'role': 'user', 'parts': [user_input]})
    history.append({'role': 'model', 'parts': [model_response]})


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