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

    def begin_today_session(self, days_offset: int = 0):
        while True:
            self.ai.start_day(days_offset=days_offset)
            cprint("\nchoose the task id you want to start with", color=User.config["notify"])
            id = input("Select id --> ")
            if id == "x" or id == "X":
                break
            elif id == "bulk":
                self.bulk_reschedule()
                pass
            else:
                try: 
                    int(id)
                    self.task_session(id)
                except Exception as e:
                    cprint("Invalid choice, try again.")
                
            #     activity = self.ai.instantiate_activity(id)
            #     self.task_session(activity)
            # # give task level options here
            # edit, start, mark completed


    def bulk_reschedule(self):
        cprint("you are in the bulk reschedule mode", color=User.config["notify"])
        ids = input("Enter all the ids you want to reschedule separated by space\n--> ")
        activity_id_list = [int(i) for i in ids.split()]
        days_in_future = int(input("how many days in the future?\t--> "))
        for activity_id in activity_id_list:
            activity = self.ai.instantiate_activity(activity_id)
            activity.query.q_activity_date_update(days_in_future)
            cprint(f"activity id {activity_id} rescheduled.",color=User.config["feedback-good"])
        pass
    
    def create_activity_session(self):
        self.ai.create_new_activity()

    def create_distributed_activity_session(self):
        cprint("you are creating a distributed bulk event")
        activity_name = input("activity name -->\t")
        print('--'*30)
        total_time = int(input("total time you want to allocate for this (hours) -->\t"))
        print('--'*30)
        num_of_days = int(input("how many days do you want to spread this over? -->\t"))
        print('--'*30)
        activity_chunk_size = input("size of each event (default 60 mins) --\t")
        print('--'*30)
        if not activity_chunk_size:
            activity_chunk_size=60
        else:
            activity_chunk_size = int(activity_chunk_size)
        num_of_days_in_future_to_start_from = input("How many days to start from in the future (default 0)-->\t")
        if not num_of_days_in_future_to_start_from:
            num_of_days_in_future_to_start_from=0
        else:
            num_of_days_in_future_to_start_from = int(num_of_days_in_future_to_start_from)
        
        u_input_incl_weekdays = input("Include weekdays [y]/n -->\t")
        if not u_input_incl_weekdays:
            incl_weekdays = True
        elif u_input_incl_weekdays == 'n':
            incl_weekdays = False
        print('--'*30)
        u_input_incl_weekends = input("Include weekends [y]/n -->\t")
        if not u_input_incl_weekends :
            incl_weekends = True
        elif u_input_incl_weekends == 'n':
            incl_weekends = False
        print('--'*30)
        
        self.ai.create_distributed_activity(
            activity=activity_name,
            total_time=total_time,
            num_of_days=num_of_days,
            activity_chunk_size=activity_chunk_size,
            num_of_days_in_future_to_start_from=num_of_days_in_future_to_start_from,
            incl_weekdays = incl_weekdays,
            incl_weekends=incl_weekends,
        )

    def lookback_session(self):
        self.ai.look(direction='back')
        
    def lookahead_session(self):
        self.ai.look(direction="ahead")

    def task_session(self, id: int):
        activity_session = ActivitySessionHandler(id)
        activity_session.orchestrate()

    def explore(self):
        explore_session = ExploreSessionHandler()
        explore_session.orchestrate()
