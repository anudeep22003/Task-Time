from typing import Callable
from termcolor import cprint
from activity import ActivityInterfacer, Activity
from stopwatch import Timer
import time


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
        pass

        pass


    def create_activity_session(self):
        self.ai.create_new_activity()

    def lookback_session(self):
        self.ai.lookback()

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
            cprint("choose from one of the  following options", color="red")
            cprint(
                "b: begin task\te: edit task\ts: set status\tr: reschedule task to another day\tx: exit",
                color="yellow",
            )
            choice = input("Make selection\t--> ")
            if choice == "b":
                ActivitySession(activity)
                break
            if choice == "e":
                activity.activity_edit()
                break
            if choice == "s":
                cprint(f"Current status\t--> {activity.status}", color="yellow")
                activity.set_status()
                break
            if choice == "r":
                activity.change_date()
                break
            if choice == "x":
                break




class ActivitySession:
    def __init__(self, activity: Activity) -> None:
        self.activity = activity
        self.session_start_time = time.time()

        self.timer = Timer(
            length_of_time=activity.time_allocated,
            start_time=self.session_start_time,
            units="mins",
        )

        self.orchestrate()

    def orchestrate(self):
        # print("enterred the orchestration of ActivitySession")
        try:
            self.activity.set_status(user_set_status="ACTIVE")
            time_done = self.timer.stopwatch_orchestrator()
            if time_done is True:
                cprint("Timer ran down.")
                self.activity.activity_end_flow()
            else:
                cprint(
                    f"Only {round((self.activity.time_allocated/self.timer.multiplier),1)} of {time_done}mins done."
                )
                self.activity.activity_end_flow()
                #! this is going into an endless loop
                
                # if self.activity.activity_end_flow() is not None:
                #     self.duplicator(
                #                 activity = f"DUPLICATED + {self.activity.activity}", 
                #                 allocated_time = self.activity.time_allocated, 
                #                 days_in_future = 1,
                #                 creator=f"task id {self.activity.id}"                         
                #     )
                    
        except Exception as e:
            self.activity.set_status(user_set_status="PAUSED")
            print(e)
