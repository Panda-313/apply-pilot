from enum import Enum

class AllowedActions(str, Enum):
    RESUME = "resume",
    EXIT = "exit",
    FEEDBACK = "feedback",
