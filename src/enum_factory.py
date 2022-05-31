from enum import Enum, auto

class User():
    details = {
        'name': "Anudeep"
    }
    
    config = {
        'notify': 'red',
        'feedback-good': 'green',
        'feedback-bad': 'red',
        'feedback-neutral': 'yellow'
    }
    
class Status(Enum):
    STARTED = auto()
    COMPLETED = auto()
    NOT_STARTED = auto()
    PAUSED = auto()

class Formatter:
    
    def __init__(self) -> None:
        pass
    
    def activity_formatter(self):
        return "{} in between {}"
    

if __name__ == "__main__":
    f = Formatter()
    print(f.activity_formatter.format("hello", "world"))