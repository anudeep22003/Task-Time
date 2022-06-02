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
        cprint("Goodmorning! Here are your tasks for the day", color = User.config["feedback-neutral"])
        while True:
            #! show my tasks for the day
            cprint("\nHere are your options: ", color=User.config["notify"])
            cprint(
                "b: Start my day \t a: Add activity \t e: End session \t l: Lookback at today \t t: Show tomorrow",
                color="yellow",
            )
            path = input("choose option\t--> ")
            if path == "e":
                cprint("ending your day. Goodnight, see you tomorrow", color="yellow")
                break
            if path == "a":
                self.session.create_activity_session()
            if path == "b":
                self.session.begin_today_session()
            if path == "l":
                self.session.lookback_session()
            if path == "t":
                self.session.lookahead_session()

        pass

    def begin_session(self):
        self.session.begin_today_session()


if __name__ == "__main__":
    u = GameManager()
