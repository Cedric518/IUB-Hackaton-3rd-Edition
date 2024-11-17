from dotenv import load_dotenv
import google.generativeai as genai

class Test:
    def __init__(self, prompt, expected):
        self.prompt = prompt
        self.expected = expected

    def __str__(self):
        
        return self.prompt == self.expected
        return f"User:{self.prompt} \n Expected Answer:{self.expected}"



class TestRunner:
    # Test that prompting works
    t1 = Test("Add Value 8487684148 to Key phone numbers", "{\"sql/\": \"INSERT INTO key_value_store (key, value, created_datetime, updated_datetime) VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)\", \"parameters\": [\"phone numbers\", \"8487684148\"]}")
    t1.check() # returns true
    # Test for filtering of prompts
    t2 = Test("\n", "")
    # Test for

