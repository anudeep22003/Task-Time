import datetime
from termcolor import cprint
from session_manager import SessionManager
from enum_factory import User


class GameManager:
    def __init__(self) -> None:
        self.session = SessionManager()
        self.ui_top_level_orchestrator()
        pass

import datetime
from termcolor import cprint
from session_manager import SessionManager
from enum_factory import User


class GameManager:
    def __init__(self) -> None:
        self.session = SessionManager()
        self.ui_top_level_orchestrator()
        pass

    def ui_top_level_orchestrator(self):

        cprint("\n------ Goodmorning and welcome to another day in the game of life. ------", color="red", on_color='on_white', end = '\n\n')
        while True:
            #! show my tasks for the day
            
            valid_choices = ['b', 'a', 'e', 't', 'ex']
            
            cprint(
                "\nOptions > \t(b)egin my day \t (a)dd activity \t (e)nd session \t (t)omorrow peek\t (ex)plore mode",
                color="yellow",
            )
            path = input("choose option\t--> ")
            if path not in valid_choices:
                cprint("Invalid choice, try another.", color='red')
            elif path == "e":
                cprint("Ending your day. Goodnight, see you tomorrow", color="yellow")
                break
            elif path == "a":
                self.session.create_activity_session()
            elif path == "b":
                self.session.begin_today_session()
            elif path == "t":
                self.session.lookahead_session()
            elif path == 'ex':
                self.session.explore()



if __name__ == "__main__":
    u = GameManager()

