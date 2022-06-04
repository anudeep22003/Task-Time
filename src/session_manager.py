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
            cprint("\nchoose the task id you want to start with", color=User.config["notify"])
            id = input("Select id --> ")
            if id == "x" or id == "X":
                break
            elif id == "bulk":
                self.bulk_reschedule()
                pass
            else:
            
                activity = self.ai.instantiate_activity(id)
                self.task_session(activity)
            # give task level options here
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
            # cprint("Here is the selected task", color="red")
            # print the task
            cprint("\n--- {} -------- {} -------- {} of {} mins done.\n".format(activity.v["id"], activity.v["activity"], activity.v["time_used"], activity.v["time_allocated"]),color=User.config["notify"])
            # show details i.e. context and notes
            activity.show_details()
            # cprint("choose from one of the  following options", color=User.config["feedback-neutral"])
            cprint(
                "\nb: begin\te: edit \ts: set status\tr: reschedule\tde: delete \tc/n: context/notes\tx: exit",
                color=User.config["feedback-neutral"],
                end = '\n'
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
            if choice == 'c' or choice == 'n':
                activity.add_context()
            if choice == "x":
                break
