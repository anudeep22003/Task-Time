from dataclasses import dataclass
from datetime import date, timedelta
from email.utils import collapse_rfc2231_value
from termcolor import cprint
import functools
from enum_factory import User

from query_factory import SqlActivityDetailsQueryFactory, SqlActivityQueryFactory, SqlGeneralQueryFactory
from stopwatch import Timer

import time


class ActivityInterfacer:
    def __init__(self) -> None:
        self.query = SqlGeneralQueryFactory()
        pass

    def delete_activity(self, id: int):
        self.query.q_delete_activity(id)
    
    def create_new_activity(self, 
                            creator="Anudeep" 
                            ):
        while True:
            row = []
            activity = input("what is the activity \t (press 'x' to exit)\t--> ")
            if activity.lower() == "x":
                break
            allocated_time = input("how much time? \t--> ")
            print("\n", end="")
            created_by = creator
            activity_date = date.today() + timedelta(days=0)
            status = "NOT_STARTED"
            time_used = 0

            row.extend(
                [created_by, activity, allocated_time, "", status, activity_date, time_used]
            )

            self.query.q_insert_row(payload = row)

    def start_day(self):
        print(
            "{:^10s}\t{:^10s}\t{:<10s}\t{:<20s}".format(
                "id", "time", "status", "activity"
            )
        )
        print("{:*^10s}\t{:*^10s}\t{:*<10s}\t{:*<20s}".format("", "", "", ""))
        for row in self.query.read_rows_by_status(status="INCOMPLETE"):
            id, activity, time_allocated, status, time_used = row
            time_string = f"{time_used} / {time_allocated}"
            print(
                "{:^10s}\t{:^10s}\t{:<10s}\t{:<20s}".format(
                    str(id), str(time_string), status, activity
                )
            )

    def look(self, direction:str = "back"):
        print(
            "{:^10s}\t{:^10s}\t{:<10s}\t{:<20s}".format(
                "id", "time", "status", "activity"
            )
        )
        print("{:*^10s}\t{:*^10s}\t{:*<10s}\t{:*<20s}".format("", "", "", ""))
        
        if direction == 'back':
            data = self.query.read_rows_by_status(status="COMPLETED")
        else:
            data = self.query.read_rows_by_status(status="INCOMPLETE", days_offset=1)
        
        for row in data:
            id, activity, time_allocated, status, time_used = row
            time_string = f"{str(time_used)} / {str(time_allocated)}"
            print(
                "{:^10s}\t{:^10s}\t{:<10s}\t{:<20s}".format(
                    str(id), str(time_string), status, activity
                )
            )
        pass

    def instantiate_activity(self, id: int):
        # print("entered here")
        return Activity(id=id)


@dataclass
class Activity:
    
    
    
    def __init__(self, id: int) -> None:
        self.id = id
        self.general_query = SqlGeneralQueryFactory()
        self.query = SqlActivityQueryFactory(id = self.id)
        self.query_details = SqlActivityDetailsQueryFactory(id)
        self.timer = Timer
        
        self.v = self.set_reset_value(initialize=True)
        
        pass
    
    

    def set_reset_value(self, initialize:bool = False):
        keys, output = self.general_query.return_activity_row(id=self.id, include_keys=True)
        if initialize:
            return dict(zip(keys, output[0]))
        else:
            self.v = dict(zip(keys, output[0]))
    
    #! currently unused
    def update_dict_decorator(self, fn):
        @functools.wraps(fn)
        def update_decorator(*args, **kwargs):
            value_from_og_fn = fn(*args, **kwargs)
            self.v = self.initialize_dict_of_value()
            return value_from_og_fn
        return update_decorator
    
    
    def run_timer(self):
        
        """
        This function uses the timer object that was passed during initialization and runs the timer.
        - It sets the status as active when the timer starts
        - the timer returns the #mins completed based on which the output to the stdio changes
        - at the end, the 'activity_end_flow' function is called to give the user further options to end the task
        
        (if the user exits without the timer having run down, and the user doesnt set a status then the "ACTIVE" status is persisted)
        """
        
        time_allocated = int(self.v["time_allocated"])
        time_used = int(self.v["time_used"])
        
        length_of_time = time_allocated - time_used
        start_time = time.time()
        t = self.timer(length_of_time, start_time, units='mins')
        # change status to active 
        self.set_status(user_set_status='ACTIVE')
        # start timer
        time_used = t.stopwatch_orchestrator()
        
        print(f"time used is {time_used}")
        # update the table with the time used
        self.query.q_activity_update_time_used(time_used)
        self.set_reset_value()
        print("Time used is updated, and values refreshed.\n")

        # if timer runs down, ask user to set status
        if time_used != time_allocated:
            cprint(f"Only {time_used} of {time_allocated} mins done.")
            self.activity_end_flow()
        else:
            self.activity_end_flow()
            
        
        

    def activity_edit(self):
        """
        
        Allows the user to edit the activity. 
        - Takes input from the user via the stdio (and allows blank input to keep the same data)
        - Once the payload is constructed it is passed to the query class to build and execute the query
        
        """
        
        cprint("You are now editing a task (x: to exit)", color="yellow")
        cprint(
            "Enter new activity description (or press enter to leave unchanged)",
            color="yellow",
        )
        new_activity = input("Enter\t--> ")
        if new_activity == "x" or new_activity == "X":
            return None
        cprint(
            "Enter new allocated time (or press enter to leave unchanged)",
            color="yellow",
        )
        new_time = input("Time\t--> ")
        if new_time == "x" or new_time == "X":
            return None

        # check for empty returns
        if new_activity == "":
            new_activity = self.v["activity"]
        if new_time == "":
            new_time = self.v["time_allocated"]

        # run an update query and inform on status of completion
        if self.query.q_activity_edit(new_activity, new_time):
            cprint("Succesfully updated", color="green")
        else:
            cprint("Failed try again", color="red")

        pass

    def update_time(self):
        while True:
            cprint(
                "Enter additional time needed (or press enter to leave unchanged)",
                color="yellow",
            )
            extra_time = input("Time\t--> ")
            if extra_time == "x" or extra_time == "X":
                break

            try:
                extra_time = int(extra_time)
                if self.query.q_activity_edit(
                    self.v["activity"],
                    updated_time=self.v["time_allocated"] + extra_time,
                ):
                    cprint("Succesfully updated time", color="green")
                    break
                else:
                    cprint("Failed try again", color="red")

            except Exception as e:
                cprint(f"Exception {e}. Try again, please enter integer value.")

    
    
    def set_status(self, user_set_status=None):

        status = {"c": "COMPLETED", "n": "NOT_STARTED", "p": "PAUSED", "a": "ACTIVE"}
        valid_choices = ["c", "n", "p", "a", "x"]

        while True:

            if user_set_status in status.values():
                if self.query.q_activity_status_update(status=user_set_status):
                    self.set_reset_value()
                    cprint(f"status updated to {user_set_status} and values refreshed.", color="green")
                    break
                else:
                    cprint("something went wrong", color="red")
                    break

            # cprint(f"Current status\t--> {self.status}", color='yellow')
            cprint("Set new status", color="yellow")
            cprint(
                "Options:\n c: COMPLETED\tn: NOT STARTED\tp: PAUSED\ta: ACTIVE\tx: Exit",
                color="yellow",
            )
            choice = input("Enter choice\t--> ")
            if choice not in valid_choices:
                print("invalid choice try again")
            elif choice == "x":
                break
            else:
                # update the status
                if self.query.q_activity_status_update(status[choice]):
                    self.set_reset_value()
                    cprint(f"status updated to {status[choice]} and values refreshed", color="green")
                    break
                else:
                    cprint("something went wrong", color="red")
                    break

    def change_date(self):
        while True:
            cprint("Reschedule to how many days in future?", color="yellow")
            days_in_future = input("Enter #days in future\t--> ")
            if days_in_future == "x":
                break
            try:
                days_in_future = int(days_in_future)
                # update date
                if self.query.q_activity_date_update(days_in_future):
                    self.set_reset_value()
                    cprint(
                        f"Rescheduled to #{days_in_future} days in the future and values updated.",
                        color="green"
                    )
                    break
                else:
                    cprint("something went wrong", color="red")
                    break

            except Exception as e:
                cprint(
                    f"Exeption: {e} \nWrong format - try again, enter integer",
                    color="red",
                )

    def activity_end_flow(self):

        """
        When a task is completed, you have the following options
        - mark completed / incomplete
        - request extra time
        - add context / notes
        - schedule a follow-up for next day
        """
        cprint("Timer ran out. Here are your options:", color="yellow")
        valid_options = ["s", "t", "c", "d", "x"]
        while True:
            cprint(
                "s: Set status\tt: more time needed\tc: add context/notes\td: duplicate to tomorrow\tx: done and exit",
                color="yellow",
            )
            choice = input("Enter choice\t--> ")
            if choice not in valid_options:
                cprint("Invalid choice try again", color="red")
            elif choice == "x":
                # set status as done
                # self.set_status(user_set_status='COMPLETED')
                self.show_feedback()
                # option here to have an out, will remove after
                break
            elif choice == "s":
            
                cprint("Current status\t--> {}".format(self.v["status"]), color="yellow")
                self.set_status()

            elif choice == "t":
                self.update_time()

            elif choice == "c":
                # add context
                print("TODO: option not yet added")
                self.add_context()
                pass

            elif choice == "d":
                self.create_daughter_event()

            # mark status

            # request extra time

            # add context / notes

            # copy to tomorrow

            pass

    def show_feedback(self):
        keys = ["#Activities", "Total time", "Average time"]
        response = self.general_query.q_sum_of_time(date=self.v["date"])
        for r in response:
            for k, v in zip(keys, r):
                cprint(f"{k}: {v}\t", end="", color="green")
            print("\n")

    def show_details(self):
        for row in self.query_details.show_details():
            context, notes = row
            cprint(f"CONTEXT: {context}\nNOTES: {notes}",color = 'red', on_color="on_yellow")

    def add_context(self):
        while True:
            valid_options = ["c", "n", "x"]

            # add context or notes
            cprint("(c) Add context\t (n) Add notes\t (x) Exit", color="yellow")
            choice = input("Enter choice\t--> ")
            if choice not in valid_options:
                cprint("Invalid choice; try again", color="red")
            elif choice == "x":
                break
            elif choice == "c":
                while True:
                    # add context
                    cprint("\nEnter the context here", color="yellow")
                    user_input_context = input("Enter here\t--> ")
                    if user_input_context == 'x':
                        break
                    self.query_details.q_add_context_notes(context = user_input_context)
                    # cprint("Added context in", color=User.config["feedback-good"])

            elif choice == "n":
                while True:
                    # add a note
                    cprint("\nEnter the notes here", color="yellow")
                    note = input("Enter here\t--> ")
                    if note == 'x':
                        break
                    self.query_details.q_add_context_notes(notes=note)
        self.show_details()
                
    
    def create_activity(self, activity: str = None, days_offset:int = 1):
        
        row = []
        if activity is None:
            activity = self.v["activity"]
        allocated_time = self.v["time_allocated"]
        created_by = self.id
        activity_date = date.today() + timedelta(days=days_offset)
        status = "NOT_STARTED"
        time_used = 0
        
        row.extend([created_by, activity, allocated_time, "", status, activity_date, time_used])
        self.general_query.q_insert_row(payload=row)

    def create_daughter_event(self):
        
        # interface with the user
        valid_choices = ["1","2","3", 'x']
        while True:
            cprint("1: create related event \t 2: duplicate event to tomorrow \t 3: duplicate to x days in the future", color=User.config['feedback-neutral'])
            
            choice = input("Enter choice --> ")
            if choice not in valid_choices:
                cprint("Invalid choice, try again.")
            elif choice == 'x':
                break
            else:
                choice = int(choice)
            if choice == 1:
                cprint("current: {}\n enter new: --> ".format(self.v["activity"]), color = User.config["feedback-neutral"], end = '')
                related_activity = input (" ")
                if related_activity == 'x':
                    pass
                else:
                    self.create_activity(activity=related_activity)
            elif choice == 2:
                self.create_activity()
                cprint("Activity duplicated to tomorrow", color=User.config['feedback-neutral'])
            elif choice == 3:
                num_days_in_future = input("How many days in future \t --> ")
                if num_days_in_future == 'x':
                    pass
                else:
                    self.create_activity(days_offset=int(num_days_in_future))
                    cprint(f"Activity duplicated to {num_days_in_future} in future", color=User.config['feedback-neutral'])
                        
            # option to copy the event as is 
            # option to change time 
            # create a different but related daughter event
        
        pass

