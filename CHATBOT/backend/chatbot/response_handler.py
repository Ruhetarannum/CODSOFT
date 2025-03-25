import json
import random
import os
from string import Template
from datetime import datetime

class ResponseHandler:
    def __init__(self, responses_file, api_key=None, debug=False):
        self.responses = self._load_responses(responses_file)
        self.weather_api_key = api_key or os.environ.get("WEATHER_API_KEY", "")
        self.debug = debug
        self._initialized = bool(self.responses)

    def _load_responses(self, file_path):
        """ Load the response templates from the JSON file. """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                print(f"DEBUG: Loaded responses JSON -> {data}")  # Debug statement
                if not isinstance(data, dict):
                    raise ValueError("ERROR: responses.json must be a dictionary, but found a list.")
                return data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR: Failed to load responses file -> {e}")
            return {}


    def generate_response(self, intent, entities=None, conversation_state=None):
        try:
            if entities is None:
                entities = {}
            if conversation_state is None:
                conversation_state = {}

            print(f"DEBUG: Intent received -> {intent}")
            print(f"DEBUG: Available responses keys -> {self.responses.keys()}")

            # Get response templates for the intent
            response_options = self.responses.get(intent, [])
            
            print(f"DEBUG: Retrieved response options -> {response_options}")

            if not isinstance(response_options, list):
                print("ERROR: Response options is not a list!")
                raise ValueError("Response options must be a list of dictionaries.")

            # Select a random response template
            if response_options:
                response_template = random.choice(response_options)
                print(f"DEBUG: Selected response template -> {response_template}")
            else:
                response_template = {"text": "I'm not sure how to respond to that."}

            response_text = response_template["text"]
            return response_text, conversation_state

        except Exception as e:
            print(f"ERROR: Response generation failed -> {str(e)}")
            return "I'm having trouble understanding. Please try again.", conversation_state

