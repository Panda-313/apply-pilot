from enum import Enum

class AllowedActions(str, Enum):
    RESUME = "resume"
    EXIT = "exit"
    FEEDBACK = "feedback"
    SEND_MESSAGE = "send_message"
