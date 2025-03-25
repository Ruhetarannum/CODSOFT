class StateManager:
    def __init__(self):
        self.conversations = {}
    
    def get_state(self, user_id):
        """
        Get the current conversation state for a user
        
        Args:
            user_id (str): The user identifier
            
        Returns:
            dict: The current conversation state
        """
        if user_id not in self.conversations:
            self.conversations[user_id] = {
                'current_intent': None,
                'entities': {},
                'context': {},
                'history': []
            }
        
        return self.conversations[user_id]
    
    def update_state(self, user_id, new_state):
        """
        Update the conversation state for a user
        
        Args:
            user_id (str): The user identifier
            new_state (dict): The new conversation state
        """
        # Add the current state to history
        if user_id in self.conversations:
            history = self.conversations[user_id].get('history', [])
            # Only store current_intent in history to avoid growing too large
            if self.conversations[user_id].get('current_intent'):
                history.append({
                    'intent': self.conversations[user_id]['current_intent'],
                    'entities': self.conversations[user_id].get('entities', {})
                })
            
            # Limit history size
            if len(history) > 10:
                history = history[-10:]
            
            new_state['history'] = history
        
        self.conversations[user_id] = new_state
    
    def reset_state(self, user_id):
        """
        Reset the conversation state for a user
        
        Args:
            user_id (str): The user identifier
        """
        self.conversations[user_id] = {
            'current_intent': None,
            'entities': {},
            'context': {},
            'history': []
        }