from enum_factory import User, Status

from termcolor import cprint
from activity.activity import Activity
from activity.activity_helper import ActivityInterfacer, ActivitySessionHandler, ExploreSessionHandler


class SessionManager:
    def __init__(self) -> None:
        self.ai = ActivityInterfacer()
        pass

    def ui_session_orchestrator(self):
        cprint("Goodmorning! Here are your tasks for the day")
        self.ai.start_day()

    def begin_today_session(self):
        while True:
            self.ai.start_day()
            cprint("\nchoose the task id you want to start with", color=User.config["notify"])
            id = input("Select id --> ")
            if id == "x" or id == "X":
                break
            elif id == "bulk":
                self.bulk_reschedule()
                pass
            else:
                
                self.updated_task_session(id)
                
            #     activity = self.ai.instantiate_activity(id)
            #     self.task_session(activity)
            # # give task level options here
            # edit, start, mark completed


    def bulk_reschedule(self):
        cprint("you are in the bulk reschedule mode", color=User.config["notify"])
        ids = input("Enter all the ids you want to reschedule separated by space\n--> ")
        activity_id_list = [int(i) for i in ids.split()]
        days_in_future = int(input("how many days in teh future?\t--> "))
        for activity_id in activity_id_list:
            activity = self.ai.instantiate_activity(activity_id)
            activity.query.q_activity_date_update(days_in_future)
            cprint(f"activity id {activity_id} rescheduled.",color=User.config["feedback-good"])
        pass
    
    def create_activity_session(self):
        self.ai.create_new_activity()

    def lookback_session(self):
        self.ai.look(direction='back')
        
    def lookahead_session(self):
        self.ai.look(direction="ahead")

    def updated_task_session(self, id: int):
        activity_session = ActivitySessionHandler(id)
        activity_session.orchestrate()

    def explore(self):
        explore_session = ExploreSessionHandler()
        explore_session.orchestrate()
