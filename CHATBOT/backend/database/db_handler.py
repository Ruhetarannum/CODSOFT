import os
import json
import datetime

class DBHandler:
    def __init__(self, db_file="database/chatbot_logs.json"):
        """Initialize the JSON-based database handler."""
        self.db_file = db_file
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        """Ensure the JSON database file exists."""
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump({"users": {}, "conversations": []}, f)

    def _load_db(self):
        """Load JSON database file."""
        try:
            with open(self.db_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"users": {}, "conversations": []}

    def _save_db(self, data):
        """Save data back to the JSON file."""
        with open(self.db_file, 'w') as f:
            json.dump(data, f, indent=2)

    def get_user(self, user_id):
        """Retrieve user data."""
        data = self._load_db()
        return data["users"].get(user_id, None)

    def create_or_update_user(self, user_id, metadata=None):
        """Create a new user or update existing user data."""
        data = self._load_db()
        
        if user_id not in data["users"]:
            data["users"][user_id] = {
                "first_seen": datetime.datetime.now().isoformat(),
                "last_seen": datetime.datetime.now().isoformat(),
                "metadata": metadata or {}
            }
        else:
            data["users"][user_id]["last_seen"] = datetime.datetime.now().isoformat()
            if metadata:
                data["users"][user_id]["metadata"] = metadata
        
        self._save_db(data)

    def log_conversation(self, user_id, user_message, bot_response, intent):
        """Log a conversation interaction."""
        self.create_or_update_user(user_id)
        data = self._load_db()

        log_entry = {
            "user_id": user_id,
            "timestamp": datetime.datetime.now().isoformat(),
            "user_message": user_message,
            "bot_response": bot_response,
            "intent": intent
        }
        
        data["conversations"].append(log_entry)
        self._save_db(data)

    def get_conversation_history(self, user_id, limit=10):
        """Retrieve conversation history for a user."""
        data = self._load_db()
        conversations = [c for c in data["conversations"] if c["user_id"] == user_id]
        return conversations[-limit:]