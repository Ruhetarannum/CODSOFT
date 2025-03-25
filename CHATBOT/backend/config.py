import os

class Config:
    """Application configuration settings"""

    # Flask settings
    DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 'yes')
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))

    # Database settings
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get backend/ directory
    DATABASE_URI = os.path.join(BASE_DIR, "database", "chatbot.db")  # Correct path

    # Chatbot settings
    DEFAULT_CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', 0.5))
    MAX_CONVERSATION_HISTORY = int(os.getenv('MAX_CONVERSATION_HISTORY', 10))
