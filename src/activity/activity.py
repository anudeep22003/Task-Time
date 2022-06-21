from dataclasses import dataclass
from datetime import date, timedelta
from pprint import pprint
from termcolor import cprint
import functools
from enum_factory import User
from query_factory import SqlActivityDetailsQueryFactory, SqlActivityQueryFactory, SqlGeneralQueryFactory
# from stopwatch import Timer

import time





@dataclass
class Activity:
    
    
    
    def __init__(self, id: int) -> None:
        self.id = id
        self.general_query = SqlGeneralQueryFactory()
        self.query = SqlActivityQueryFactory(id = self.id)
        self.query_details = SqlActivityDetailsQueryFactory(id)
        # self.timer = Timer
        
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
                
        
        
    @update_values
    def activity_edit(self, 
                              new_act_description:str, 
                              new_act_time: str):
        
        # generate default values if user presses enter without entering anything
        if not new_act_description:
            new_act_description = self.v["activity"]
        
        if not new_act_time:
            new_act_time = self.v["time_allocated"]
        
        return self.query.q_activity_edit(new_act_description, new_act_time)
    

    @update_values
    def update_time(self, extra_time: int):
        self.query.q_add_time(extra_time)
    
    @update_values
    def set_status(self, status: str):
        self.query.q_activity_status_update(status)

    @update_values
    def change_date(self, days: int):
        self.query.q_activity_date_update(days_offset=days)
    
    def add_context(self, context: str):
        self.query_details.q_add_context(context=context)
        
    def add_notes(self, note: str):
        self.query_details.q_add_notes(notes=note)


    def create_activity(self, activity: str = "", days_offset:int = 1, allocated_time:int = 0):
        
        row = []
        if not activity:
            activity = self.v["activity"]
        if not allocated_time:
            allocated_time = self.v["time_allocated"]
        created_by = self.id
        activity_date = date.today() + timedelta(days=days_offset)
        status = "NOT_STARTED"
        time_used = 0
        
        row.extend([created_by, activity, allocated_time, "", status, activity_date, time_used])
        daughter_id = self.general_query.q_insert_row(payload=row)
        
        # initialize the details table with the prior context and notes
        daughter_details = SqlActivityDetailsQueryFactory(parent_activity_id = daughter_id)
        
        # the user can only add notes, the notes are copied into the context of the daughter
        daughter_details.initialize_daughter_details(
            context= self.query_details.get_notes()
        )
        


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
                cprint(f"__Context:__", color = "grey", on_color= "on_green", end = '\n')
                cprint(f"{context}", color = User.config["feedback-good"], end = '\n\n')
                cprint(f"__Notes:__", color = "grey", on_color= "on_green", end = '\n')
                cprint(f"{notes}", color = User.config["feedback-good"], end = '\n')

    
                
    


