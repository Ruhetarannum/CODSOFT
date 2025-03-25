from dataclasses import dataclass
from typing import Dict, Any, Optional
import datetime

@dataclass
class User:
    id: str
    first_seen: str
    last_seen: str
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class Conversation:
    id: int
    user_id: str
    timestamp: str
    user_message: str
    bot_response: str
    intent: str