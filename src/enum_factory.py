from enum import Enum, auto

class User():
    details = {
        'name': "Anudeep"
    }
    
class Status(Enum):
    STARTED = auto()
    COMPLETED = auto()
    NOT_STARTED = auto()
    PAUSED = auto()
    