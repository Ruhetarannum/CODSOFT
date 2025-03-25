import json
import re
from .nlp_utils import preprocess_text, extract_entities, normalize_text

class PatternMatcher:
    def __init__(self, patterns_file):
        self.patterns = self._load_patterns(patterns_file)
        
    def _load_patterns(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading patterns file: {e}")
            return {}
    
    def match(self, text, conversation_state=None):
        """
        Match the input text to an intent pattern
        
        Args:
            text (str): User input text
            conversation_state (dict): Current conversation state
            
        Returns:
            tuple: (intent_name, confidence_score, extracted_entities)
        """
        # Preprocess input text
        preprocessed_text = preprocess_text(text)
        normalized_text = normalize_text(preprocessed_text)
        
        best_intent = None
        best_confidence = 0.0
        best_entities = {}
        
        # Check context-aware patterns first if in a specific state
        if conversation_state and 'current_intent' in conversation_state:
            current_intent = conversation_state['current_intent']
            followup_patterns = self.patterns.get('followups', {}).get(current_intent, [])
            
            for pattern_info in followup_patterns:
                pattern = pattern_info['pattern']
                
                # Regex pattern matching
                if pattern.startswith('^') and pattern.endswith('$'):
                    match = re.match(pattern, normalized_text, re.IGNORECASE)
                    if match:
                        confidence = 1.0  # Exact regex match
                        entities = extract_entities(match, pattern_info.get('entities', []))
                        return pattern_info['intent'], confidence, entities
                
                # Keyword matching
                elif pattern.lower() in normalized_text:
                    confidence = 0.9  # Contains exact phrase
                    entities = extract_entities(text, pattern_info.get('entities', []))
                    if confidence > best_confidence:
                        best_intent = pattern_info['intent']
                        best_confidence = confidence
                        best_entities = entities
        
        # Check global patterns
        for intent_name, patterns_list in self.patterns.get('intents', {}).items():
            for pattern_info in patterns_list:
                pattern = pattern_info['pattern']
                
                # Regex pattern matching
                if pattern.startswith('^') and pattern.endswith('$'):
                    match = re.match(pattern, normalized_text, re.IGNORECASE)
                    if match:
                        confidence = 0.95  # Exact regex match
                        entities = extract_entities(match, pattern_info.get('entities', []))
                        return intent_name, confidence, entities
                
                # Keyword matching
                elif pattern.lower() in normalized_text:
                    # Calculate confidence based on pattern coverage
                    pattern_words = set(pattern.lower().split())
                    input_words = set(normalized_text.split())
                    
                    if pattern_words and input_words:
                        overlap = pattern_words.intersection(input_words)
                        coverage = len(overlap) / len(pattern_words)
                        confidence = 0.5 + (coverage * 0.4)  # Scale from 0.5 to 0.9
                    else:
                        confidence = 0.5
                    
                    entities = extract_entities(text, pattern_info.get('entities', []))
                    
                    if confidence > best_confidence:
                        best_intent = intent_name
                        best_confidence = confidence
                        best_entities = entities
        
        # If no match, return fallback intent
        if best_intent is None:
            return "fallback", 0.0, {}
            
        return best_intent, best_confidence, best_entities