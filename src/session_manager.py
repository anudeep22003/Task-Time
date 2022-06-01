from enum_factory import User, Status

from termcolor import cprint
from activity import ActivityInterfacer, Activity


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
            cprint("choose the task id you want to start with", color="red")
            id = input("Select id --> ")
            if id == "x" or id == "X":
                break
            activity = self.ai.instantiate_activity(id)
            self.task_session(activity)
            # give task level options here
            # edit, start, mark completed


    def create_activity_session(self):
        self.ai.create_new_activity()

    def lookback_session(self):
        self.ai.look(direction='back')
        
    def lookahead_session(self):
        self.ai.look(direction="ahead")

    def task_session(self, activity: Activity):
        """
        Print the task that has been selected
        Give user following options:
        - edit task (edit description and time)
        - mark as completed
        - start task (start timer)
        - exit
        """
        while True:
            cprint("Here is the selected task", color="red")
            # print the task
            cprint("\n--- {} -------- {} -------- {} of {} mins done.\n".format(activity.v["id"], activity.v["activity"], activity.v["time_used"], activity.v["time_allocated"]),color=User.config["feedback-neutral"])
            cprint("choose from one of the  following options", color="red")
            cprint(
                "b: begin task\te: edit task\ts: set status\tr: reschedule task to another day\tde: delete task \tx: exit",
                color="yellow",
            )
            choice = input("Make selection\t--> ")
            if choice == "b":
                activity.run_timer()
                break
            if choice == "e":
                activity.activity_edit()
                break
            if choice == "s":
                cprint(f"Current status\t--> {activity.v['status']}", color="yellow")
                activity.set_status()
                break
            if choice == "r":
                activity.change_date()
                break
            if choice == 'de':
                self.ai.delete_activity(activity.id)
                cprint("deleted activity", color=User.config["feedback-bad"])
                break
            if choice == "x":
                break
