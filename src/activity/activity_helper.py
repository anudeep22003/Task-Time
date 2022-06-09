
from termcolor import cprint
from datetime import date, timedelta
from activity.activity import Activity
from query_factory import SqlGeneralQueryFactory
from enum_factory import User


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
            "\n{:^10s}\t{:^10s}\t{:<10s}\t{:<20s}".format(
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
        
        total_aggregate = self.query.q_get_aggregate_all 
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
                "\n(b))egin\t(t)ime add\t(e)dit\t(s)tatus\t(r)eschedule\t(d)aughter\t(c)ontext\t(n)otes\te(x)it",
                color=User.config["feedback-neutral"],
                end = '\n'
            )
            choice = input("-->\t")
            if choice == "b":
                #! how to handle if timer has been used
                self.activity.run_timer()
                
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
            
            try:
                days_in_future = int(days_in_future)
                self.activity.create_activity(activity_desc, days_in_future)
                
                cprint("Alert -->", end = '\t', color="red")
                if activity_desc:
                    cprint(f"{activity_desc} created a related event -- {days_in_future} days -- in the future\n")
                else:
                    cprint(f"Activity duplicated -- {days_in_future} days --  in the future\n")
                
            except Exception as e:
                cprint("Wrong value for days, enter integer", color='red')
                
                

                
                
        
    def edit_activity(self):
    
        cprint("Enter new values or press Enter to leave unchanged", color = 'yellow')
        activity_description = input("Description\t-->")
    
        cprint("Enter new allocated time (or press enter to leave unchanged)", color="yellow")    
        new_time = input("Time\t--> ")
        
        self.activity.updated_activity_edit(activity_description,new_time)

            
    def add_context(self):
        while True:
            context = input("context\t--> ")
            if context == 'x':
                return
            self.activity.updated_add_context(context)

    def add_note(self):
        while True:
            note = input("note\t--> ")
            if note == 'x':
                return
            self.activity.updated_add_context(note)
    
    def change_date(self):
        cprint("Reschedule by how many days?", color="yellow", end = '')
        days = input("\t--> ")
        if days == "x":
            return
        try:
            days = int(days)
            self.activity.updated_change_date(days)
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
        else:
            self.activity.updated_set_status(status_choices[user_status_choice])
        

    def update_time(self):
        cprint("Extra time needed",color="yellow", end = '')
        extra_time = input("\t--> ")
        if extra_time == "x":
            return
        try:
            extra_time = int(extra_time)
            self.activity.updated_update_time(extra_time)
            return 
        except Exception as e:
            cprint(f"Exeption: {e} \nWrong format for time - try again, enter integer", color="red")




if __name__ == "__main__":
    ai = ActivityInterfacer()
    ai.sum_orchestrator(-6)