import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import importlib.util
from datetime import datetime
import requests

# Get absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
patterns_path = os.path.join(DATA_DIR, 'patterns.json')
responses_path = os.path.join(DATA_DIR, 'responses.json')

# Helper function to verify JSON structure
def verify_json_file(file_path, expected_type=dict):
    """Verify that a file exists and contains valid JSON of the expected type"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            if not isinstance(data, expected_type):
                return expected_type()  # Return an empty dictionary if incorrect format
        return data
    except json.JSONDecodeError:
        return expected_type()  # Return an empty dictionary if JSON is invalid

# Load verified data files
patterns_data = verify_json_file(patterns_path, expected_type=dict)
responses_data = verify_json_file(responses_path, expected_type=dict)

# Define frontend directory
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, '../frontend'))

# Import configuration
class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATABASE_PATH = os.path.join(BASE_DIR, "database", "chatbot_logs.json")  # Updated to JSON
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', '')

# Import chatbot components
from chatbot.pattern_matcher import PatternMatcher
from chatbot.response_handler import ResponseHandler
from chatbot.state_manager import StateManager
from database.db_handler import DBHandler

# Initialize Flask app
app = Flask(__name__, static_folder=os.path.join(FRONTEND_DIR, 'static'))
CORS(app)

# Initialize components
db_handler = DBHandler(Config.DATABASE_PATH)  # Updated to use JSON
pattern_matcher = PatternMatcher(patterns_path)
response_handler = ResponseHandler(responses_data, api_key=Config.WEATHER_API_KEY, debug=Config.DEBUG)
state_manager = StateManager()

# Helper function for standardized API responses
def create_response(success, data=None, error=None):
    response = {'success': success, 'data': data or {}}
    if error:
        response['error'] = error
    return jsonify(response)

def fetch_weather(location):
    """ Fetch weather data using WeatherAPI.com """
    if not Config.WEATHER_API_KEY:
        return "Weather API key is missing."
    
    url = f"http://api.weatherapi.com/v1/current.json?key={Config.WEATHER_API_KEY}&q={location}&aqi=no"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temp = data["current"]["temp_c"]
            weather_desc = data["current"]["condition"]["text"]
            return f"The weather in {location} is {weather_desc} with a temperature of {temp}°C."
        else:
            return "Sorry, I couldn't find weather information for that location."
    except Exception:
        return "Sorry, I couldn't fetch the weather details at the moment."

@app.route('/')
def index():
    if os.path.exists(os.path.join(FRONTEND_DIR, 'index.html')):
        return send_from_directory(FRONTEND_DIR, 'index.html')
    return "Chatbot frontend not found.", 404

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        user_id = data.get('user_id', 'default_user')
        
        if not user_message:
            return create_response(False, error='Empty message received'), 400

        # Get user state
        conversation_state = state_manager.get_state(user_id)

        # Match intent
        intent, confidence, entities = pattern_matcher.match(user_message, conversation_state)
        if confidence < 0.6:
            intent = "fallback"
        
        # Handle dynamic time response
        if intent == "time_query":
            current_time = datetime.now().strftime("%I:%M %p")
            response_text = f"The current time is {current_time}."
            return create_response(True, {'response': response_text, 'intent': intent, 'confidence': confidence})
        
        # Handle weather query
        if intent == "weather_query" and "location" in entities:
            location = entities["location"]
            weather_info = fetch_weather(location)
            return create_response(True, {'response': weather_info, 'intent': intent, 'confidence': confidence})
        
        # Generate response
        response, new_state = response_handler.generate_response(intent, entities, conversation_state)
        
        # Update user state
        state_manager.update_state(user_id, new_state)
        
        # Log conversation
        db_handler.log_conversation(user_id, user_message, response, intent)

        return create_response(True, {'response': response, 'intent': intent, 'confidence': confidence})
    except Exception as e:
        return create_response(False, error='Internal server error'), 500

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host="127.0.0.1", port=8000)
