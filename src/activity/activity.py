from dataclasses import dataclass
from datetime import date, timedelta
from pprint import pprint
from termcolor import cprint
import functools
from enum_factory import User

from query_factory import SqlActivityDetailsQueryFactory, SqlActivityQueryFactory, SqlGeneralQueryFactory
from stopwatch import Timer

import time




@dataclass
class Activity:
    
    
    
    def __init__(self, id: int) -> None:
        self.id = id
        self.general_query = SqlGeneralQueryFactory()
        self.query = SqlActivityQueryFactory(id = self.id)
        self.query_details = SqlActivityDetailsQueryFactory(id)
        self.timer = Timer
        
        self.v = self.set_reset_value(initialize=True)

    

    def set_reset_value(self, initialize:bool = False):
        keys, output = self.general_query.return_activity_row(id=self.id, include_keys=True)
        if initialize:
            return dict(zip(keys, output[0]))
        else:
            self.v = dict(zip(keys, output[0]))
    
    def update_values(fn):
        @functools.wraps(fn)
        def update_values_decorator(self, *args, **kwargs):
            value_from_og_fn = fn(self, *args, **kwargs)
            
            # update the class with the new values
            self.set_reset_value()
            return value_from_og_fn
        return update_values_decorator
    
    
    def run_timer(self):
        
        """
        This function uses the timer object that was passed during initialization and runs the timer.
        - It sets the status as active when the timer starts
        - the timer returns the #mins completed based on which the output to the stdio changes
        - at the end, the 'activity_end_flow' function is called to give the user further options to end the task
        
        (if the user exits without the timer having run down, and the user doesnt set a status then the "ACTIVE" status is persisted)
        """
        
        # extracts the time allocated value from the database and converts value to an int
        time_allocated = int(self.v["time_allocated"])
        
        # extracts the time used from the db and also converts to int
        time_used = int(self.v["time_used"])
        
        # length of time is how long the timer is to run 
        # and it is the diffence between how much was allocated and how much was used 
        length_of_time = time_allocated - time_used
        
        # we set the start time as time now
        start_time = time.time()
        
        # we create a timer object with how long it is supposed to run and what the start time is
        t = self.timer(length_of_time, start_time, units='mins')
        
        # change status to active to mark that this task is currently running
        self.updated_set_status(status='ACTIVE')
        
        # we start the timer
        time_used = t.stopwatch_orchestrator()
        
        # debug 
        # print(f"{time_used} min used.")
        
        # update the time used value
        time_used = time_used + int(self.v["time_used"])
        
        # update the table with the time used
        self.query.q_activity_update_time_used(time_used)
        self.set_reset_value()
        # debug
        # print("Time used is updated, and values refreshed.\n")

        # if timer runs down, ask user to set status
        cprint(f"{time_used} of {time_allocated} mins done.")
            
        
        
    @update_values
    def updated_activity_edit(self, 
                              new_act_description:str, 
                              new_act_time: str):
        
        # generate default values if user presses enter without entering anything
        if not new_act_description:
            new_act_description = self.v["activity"]
        
        if not new_act_time:
            new_act_time = self.v["time_allocated"]
        
        return self.query.q_activity_edit(new_act_description, new_act_time)
    

    @update_values
    def updated_update_time(self, extra_time: int):
        self.query.q_add_time(extra_time)
    
    @update_values
    def updated_set_status(self, status: str):
        self.query.q_activity_status_update(status)

    @update_values
    def updated_change_date(self, days: int):
        self.query.q_activity_date_update(days_offset=days)
    
    def updated_add_context(self, context: str):
        self.query_details.q_add_context_notes(context=context)
        
    def updated_add_notes(self, note: str):
        self.query_details.q_add_context_notes(notes=note)


    def create_activity(self, activity: str = "", days_offset:int = 1):
        
        row = []
        if not activity:
            activity = self.v["activity"]
        allocated_time = self.v["time_allocated"]
        created_by = self.id
        activity_date = date.today() + timedelta(days=days_offset)
        status = "NOT_STARTED"
        time_used = 0
        
        row.extend([created_by, activity, allocated_time, "", status, activity_date, time_used])
        self.general_query.q_insert_row(payload=row)


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
            if not context and not notes:
                pass
            else:
                cprint(f"__Context:__\n{context}\n\n__Notes:__\n{notes}", color = User.config["feedback-good"], end = '\n')

    
                
    


