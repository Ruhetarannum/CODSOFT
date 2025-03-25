import re
import string

def preprocess_text(text):
    """
    Preprocess the text by removing extra whitespace and punctuation
    
    Args:
        text (str): The input text
        
    Returns:
        str: The preprocessed text
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def normalize_text(text):
    """
    Normalize text by removing punctuation and stopwords
    
    Args:
        text (str): The input text
        
    Returns:
        str: The normalized text
    """
    # Basic stopwords (expand as needed)
    stopwords = {'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 
                'and', 'or', 'but', 'if', 'then', 'else', 'when', 'up', 'down', 'in', 
                'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once'}
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove stopwords (optional for a rule-based system)
    # words = [word for word in text.split() if word not in stopwords]
    # text = ' '.join(words)
    
    return text

def extract_entities(text_or_match, entity_patterns):
    """
    Extract entities from text using regex patterns
    
    Args:
        text_or_match: The input text or regex match object
        entity_patterns (list): List of entity patterns to extract
        
    Returns:
        dict: Extracted entities
    """
    entities = {}
    
    # If input is a regex match object
    if hasattr(text_or_match, 'group'):
        # Extract named groups
        for entity_name in entity_patterns:
            try:
                value = text_or_match.group(entity_name)
                if value:
                    entities[entity_name] = value
            except IndexError:
                pass
    
    # If input is text, use regex patterns
    else:
        text = text_or_match
        for entity in entity_patterns:
            pattern = entity.get('pattern')
            name = entity.get('name')
            
            if pattern and name:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    try:
                        # Use the first capturing group or the entire match
                        entities[name] = match.group(1) if match.groups() else match.group(0)
                    except IndexError:
                        entities[name] = match.group(0)
    
    return entities