from logging import exception
import random 
from math import ceil
from termcolor import cprint
from datetime import date, timedelta
from activity.activity import Activity
from query_factory import SqlGeneralQueryFactory
from enum_factory import User
from stopwatch import Timer

class ActivityInterfacer:
    def __init__(self) -> None:
        self.query = SqlGeneralQueryFactory()
        pass

    def delete_activity(self, id: int):
        self.query.q_delete_activity(id)

    def create_distributed_activity(self, 
                                    activity: str,
                                    total_time: int,
                                    num_of_days:int, 
                                    activity_chunk_size: int = 1,
                                    num_of_days_in_future_to_start_from:int = 0,
                                    incl_weekdays: bool = True,
                                    incl_weekends: bool = False):
       """
       Takes activity parameters and distributes an activity over a certain time frame.
       Allows you to dedicate 6 hours over the next week to focus on a particular task 
       
       Parameters:
       - task_name: str
       - total_time: int --> time in hours
       - num_days: int --> to distribute over
       - num_of_days_in_future_to_start_from: int --> whether to start from today/tomorrow or more 
       - activity_chunk_size: int --> how big is each activity
       - incl_weekdays: bool --> if the sampler should take into account weekdays
       - incl_weekends: bool --> if the sampler should take into account weekends

       Method:
       Create an array of datetime objects (or strings) and randomize the array.
       Lenth of array is `num_of_days` and you will select the first n elements where n = total_time/activity_chunk_size
       
       Complication:
       - The activity should have numbering --> (5/7) Activity name 
       - the susequent activities should have the previous one be their creator 
       - You have to copy context to the next one. This will become complex. 
       """
       # based on weekends allowed or not, accumulate a list of candidate days
       candidate_event_schedule = list()

       # this is the number of events that need to created
       num_of_events = ceil(total_time*60/activity_chunk_size)
       
       # whether the first day to start event from is today or tomorrow or future
       start_day = date.today() + timedelta(days=num_of_days_in_future_to_start_from)
       day_offset = 0
       
       while len(candidate_event_schedule)<num_of_days:
           day_candidate = start_day + timedelta(days=day_offset)
           # adds the day to the candidate schedule based on weekend and weekday prefs
           if (incl_weekdays) and (day_candidate.weekday() not in [5,6]):
               candidate_event_schedule.append(day_candidate)
           if (incl_weekends) and (day_candidate.weekday() in [5,6]):
               candidate_event_schedule.append(day_candidate)
           day_offset+=1
       
       # shuffle the candidates to distribute
       random.shuffle(candidate_event_schedule)
       
       if num_of_days<num_of_events:
           additional_req_days = num_of_events - num_of_days
           cprint(f"not enough days to distribute, {additional_req_days} more days needed", color='red', on_color='on_yellow')

       else:
           schedule = candidate_event_schedule[:num_of_events]
           creator = 'Anudeep'
           for num, day in enumerate(sorted(schedule)):
               activity_string = f"({num+1}/{num_of_events}) {activity}"
               creator = self.activity_creator(activity_string,
                                               allocated_time=activity_chunk_size,
                                               creator=creator,
                                               activity_date=day,
                                               )
               cprint(f"Activity {num} created {(day-date.today()).days} days in the future.",
                      color='green', on_color='on_white')

       
    
    
    def activity_creator(self,
                         activity, 
                         allocated_time, 
                         creator: str,
                         status: str = "NOT_STARTED",
                         activity_date: date = date.today(),
    ):

        created_by = creator
        time_used = 0

        activity_row_to_insert = [created_by, activity, allocated_time, "", status, activity_date, time_used]
        return self.query.q_insert_row(payload = activity_row_to_insert)
    
    def create_new_activity(self, 
                            creator="Anudeep" 
                            ):
        while True:
            try:
                row = []
                activity = input("\nwhat is the activity \t (press 'x' to exit)\t--> ")
                if activity.lower() == "x":
                    break
                allocated_time = input("how much time? (default time = 5 mins) \t--> ")
                if allocated_time == 'x':
                    break
                if not allocated_time:
                    allocated_time = 5
                int(allocated_time)
                self.activity_creator(activity, allocated_time, creator=creator)
            except Exception as e:
                cprint("Enter integer value for time", color='red', on_color='on_yellow')

    def create_empty_activity(self, time:int = 30, creator = "Anudeep"):
        
        # create an empty activity for explore mode
        
        activity = " "
        allocated_time = time
        created_by = creator
        activity_date = date.today()
        status = "NOT_STARTED"
        time_used = 0
        
        row = [created_by, activity, allocated_time, "", status, activity_date, time_used]
        
        return self.query.q_insert_row(payload=row)
        
        
        

    def start_day(self, days_offset: int = 0):
        print(
            "\n{:^10s}\t{:^10s}\t{:<10s}\t{:<20s}".format(
                "id", "time", "status", "activity"
            )
        )
        print("{:*^10s}\t{:*^10s}\t{:*<10s}\t{:*<20s}".format("", "", "", ""))
        for row in self.query.read_rows_by_status(status="INCOMPLETE",days_offset=days_offset):
            id, activity, time_allocated, status, time_used = row
            time_string = f"{time_used} / {int(time_allocated)}"
            
            if time_allocated < 10:
                cprint(
                    "{:^10s}\t{:^10s}\t{:<10s}\t{:<20s}".format(
                        str(id), str(time_string), status, activity
                    ), on_color='on_magenta', attrs=['underline']
                )
            else:
                print(
                    "{:^10s}\t{:^10s}\t{:<10s}\t{:<20s}".format(
                        str(id), str(time_string), status, activity
                    )
                )
        print("-"*68)
        self.look_no_header()
        print("-"*68)
        self.sum_orchestrator()
        # print sums 
    
    def sum_orchestrator(self, days_offset: int = 0):
        print("{:-^10s}\t{:-^10s}\t{:-<10s}\t{:-<20s}".format("", "", "", ""))
        print("{:^10s}\t{:^10s}\t{:^10s}\t{:^20s}".format("#activities", "used", "allocated", "% used"))
        print("{:-^10s}\t{:-^10s}\t{:-<10s}\t{:-<20s}".format("", "", "", ""))
        total_aggregate = self.query.q_get_aggregate_all(days_offset)
        
        # list with only a single item is returned so manually indexing to that
        total_aggregate = total_aggregate[0]
        
        if not (None in total_aggregate):
            num_activities, total_used, total_time_allocated = total_aggregate
            print(
                "{:^10.0f}\t{:^10.0f}\t{:^10.0f}\t{:^20.2%}".format(
                    num_activities, total_used, total_time_allocated, (total_used/total_time_allocated)
                ))
        
        # total_aggregate = self.query.q_get_aggregate_all 
        pass

    def look_no_header(self, direction:str = "back"):
                
        if direction == 'back':
            data = self.query.read_rows_by_status(status="COMPLETED")
        else:
            data = self.query.read_rows_by_status(status="INCOMPLETE", days_offset=1)
        
        for row in data:
            id, activity, time_allocated, status, time_used = row
            time_string = f"{str(time_used)} / {str(int(time_allocated))}"
            if time_allocated < 10:
                cprint(
                    "{:^10s}\t{:^10s}\t{:<10s}\t{:<20s}".format(
                        str(id), str(time_string), status, activity
                    ), on_color='on_magenta', attrs=['underline']
                )
            else:
                print(
                    "{:^10s}\t{:^10s}\t{:<10s}\t{:<20s}".format(
                        str(id), str(time_string), status, activity
                    )
                )
        pass
    
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


class ActivitySessionHandler:
    def __init__(self, id:int) -> None:
        self.activity = Activity(id)
        self.timer = Timer
        pass

    
    def orchestrate(self):
        """
        Print the task that has been selected
        Give user following options:
        - edit task (edit description and time)
        - mark as completed
        - start task (start timer)
        - exit
        """
        cprint("\n--- {} -------- {} -------- {} of {} mins done.\n".format(self.activity.v["id"], self.activity.v["activity"], self.activity.v["time_used"], self.activity.v["time_allocated"]),color=User.config["notify"])
        self.activity.show_details()
        
        while True:
            # cprint("Here is the selected task", color="red")
            # print the task
            # show details i.e. context and notes
            # cprint("choose from one of the  following options", color=User.config["feedback-neutral"])
            cprint(
                "\n(b))egin\t(t)ime add\t(e)dit\t(s)tatus\t(r)eschedule\t(d)aughter\t(c)ontext [deprecated]\t(n)otes\te(x)it",
                color=User.config["feedback-neutral"],
                end = '\n'
            )
            choice = input("-->\t")
            if choice == "b":
                #! how to handle if timer has been used
                Timer(self.activity).run_timer()
                #self.activity.run_timer()
                
            if choice == "e":
                self.edit_activity()
                break
            if choice == "s":
                cprint(f"Current status\t--> {self.activity.v['status']}", color="yellow")
                self.set_status()
                break
            if choice == "r":
                self.change_date()
                break
            
            if choice == 'c':
                self.add_context()
                # show the details after you added some in
                self.activity.show_details()
            
            if choice == 'n':
                self.add_note()
                # show the details after you added some in
                self.activity.show_details()
            if choice == "x":
                break
            if choice == 't':
                self.update_time()
            if choice == 'd':
                self.create_daughter()

            
    def create_daughter(self):
        
        cprint("Create related activity or duplicate event", color='yellow')
        while True:
            
            activity_desc = input("related activity (default: current activity) -->\t")
            
            if activity_desc == 'x':
                break
            
            days_in_future = input("num days in future? (default: 1 day) \t--> ")
            
            if days_in_future == 'x':
                break
            
            if not days_in_future:
                days_in_future = 1
            
            allocated_time = input("Time you need for the event? (default: {} mins) \t--> ".format(self.activity.v["time_allocated"]))
            
            if allocated_time == 'x':
                break
            
            if not allocated_time:
                allocated_time = 0
            
            try:
                days_in_future = int(days_in_future)
                allocated_time = int(allocated_time)
                
                self.activity.create_activity(activity_desc, days_in_future,allocated_time)
                
                cprint("Alert -->", end = '\t', color="red")
                if activity_desc:
                    cprint(f"[{activity_desc}] created a daughter event [{activity_desc}] -- {days_in_future} days -- in the future\n")
                else:
                    cprint(f"Activity duplicated -- {days_in_future} days --  in the future\n")
                
            except Exception as e:
                cprint(f"{e}! Wrong value for days, enter integer", color='red')
                
                

                
                
        
    def edit_activity(self):
    
        cprint("Enter new values or press Enter to leave unchanged", color = 'yellow')
        activity_description = input("Description -->\t")
    
        cprint("Enter new allocated time (or press enter to leave unchanged)", color="yellow")    
        new_time = input("Time -->\t")
        
        self.activity.activity_edit(activity_description,new_time)

            
    def add_context(self):
        while True:
            context = input("context\t--> ")
            if context == 'x':
                return
            self.activity.add_context(context)

    def add_note(self):
        while True:
            note = input("note\t--> ")
            if note == 'x':
                return
            self.activity.add_notes(note)
    
    def change_date(self):
        cprint("Reschedule by how many days?", color="yellow", end = '')
        days = input("\t--> ")
        if days == "x":
            return
        try:
            days = int(days)
            self.activity.change_date(days)
            return
        except Exception as e:
            cprint(f"Exeption: {e} \nWrong format for #days - try again, enter integer", color="red")
    

    def set_status(self):
        status_choices = {"c": "COMPLETED", "n": "NOT_STARTED", "p": "PAUSED", "a": "ACTIVE"}
        
        cprint(
            "\n c: COMPLETED\tn: NOT STARTED\tp: PAUSED\ta: ACTIVE\tx: Exit",
            color="yellow",
        )
        user_status_choice = input("-->\t")
        if user_status_choice == 'x':
            return
        elif not user_status_choice in status_choices.keys():
            cprint("Out of scope choice, try again", color='red')
        elif user_status_choice == 'c':
            allocated_time = int(self.activity.v["time_allocated"])
            user_input_time = input("Enter time used (default = {})".format(allocated_time))
            if not user_input_time:
                user_input_time = allocated_time
            else:
                try:
                    user_input_time = int(user_input_time) 
                except ValueError:
                    print("enter appropriate numeric value for time")
            self.activity.update_time_used(user_input_time)
            self.activity.set_status(status_choices[user_status_choice])
        else:
            self.activity.set_status(status_choices[user_status_choice])
        

    def update_time(self):
        cprint("Extra time needed",color="yellow", end = '')
        extra_time = input("\t--> ")
        if extra_time == "x":
            return
        try:
            extra_time = int(extra_time)
            self.activity.update_time(extra_time)
            return 
        except Exception as e:
            cprint(f"Exeption: {e} \nWrong format for time - try again, enter integer", color="red")


class ExploreSessionHandler:
    
    """
    This class is going to handle the user interface for the explore mode. 
    
    To do this you will need:
    - Once you enter the explore mode, tell user so 
    - The user chooses to start timer for 30-60-120 min session 
    - User can end it wheneverk, but when they do they can:
        - Ask for more time and get back to activity 
        - Add the activitiy description 
    - then they can end the session if they want or continue it / add time to it 
    """
    
    def __init__(self) -> None:
        self.ai = ActivityInterfacer()
        pass
    
    def assign_activity(self,id: int):
        return Activity(id)

    def orchestrate(self):
        cprint("\n------| You are now in explore mode |------\n", color= 'yellow')
        # show tasks timed so far
        
        while True:
            # report of the tasks explored today
            self.ai.look(direction='back')
            self.ai.sum_orchestrator()

            id = self.create_shell_activity()
            if id is None:
                break
            
            activity = self.assign_activity(id)
            # run the timer
            self.activity_run_timer(activity)
            
    
    def add_activity_desc(self, activity: Activity):
        while True:
            cprint("Enter description of activity", color = 'yellow')
            description = input("--> ")
            if description == 'x':
                break
            else:
                activity.activity_edit(new_act_description=description)
                break
                
    def activity_run_timer(self, activity: Activity):
        cprint("Starting timer\n", color='yellow')
        t = Timer(activity)
        t.run_timer()
        # activity.run_timer()
        self.end_flow(activity)
        

    def activity_add_time(self, activity: Activity):
        while True:
            cprint("how much more time?")
            try:
                time = int(input("--> "))
                activity.update_time(time)

                # continue the timer
                break
            
            except Exception as e:
                print("invalid choice, try again.")

    def create_shell_activity(self):
        while True:
            cprint("\n----- Choose session size in mins (default 30 mins) ----- ", color='yellow')
            user_size = input('-->\t')
            if user_size == 'x':
                return None
            if not user_size:
                user_size = 30
            
            try:
                session_size = int(user_size)
                
                # create an empty activity
                
                id = self.ai.create_empty_activity(time=session_size)
                return id
                
            except Exception as e:
                print(e)
    
    def activity_exit(self, activity: Activity):
        # update status to done 
        activity.set_status(status = 'COMPLETED')
        
    
    def end_flow(self, activity: Activity):
        valid_choices = ['t', 'd', 'c', 'x']
        while True:
            cprint("d: done, add description\t t: add time\t c: continue timer\t x: exit, next activity", color='yellow')
            choice = input("--> ")
            if choice not in valid_choices:
                cprint("Out of bound choice, try again", color='red')
            if choice == 'd':
                self.add_activity_desc(activity)
            if choice == 't':
                self.activity_add_time(activity)
            if choice == 'c':
                self.activity_run_timer(activity)
            if choice == 'x':
                # exit and set the right status
                self.activity_exit(activity)
                break



if __name__ == "__main__":
    ai = ActivityInterfacer()
    ai.sum_orchestrator(-6)