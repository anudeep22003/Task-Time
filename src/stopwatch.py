from audioop import mul
import time
from tracemalloc import start
from typing import Callable
from termcolor import cprint
from pydub import AudioSegment
from pydub.playback import play

from activity.activity import Activity





class Timer:
    def __init__(self,
                activity: Activity,
                # time_allocated,
                # time_used: int, 
                # time_left_to_run: float, 
                # start_time: time,
                # time_update_fn: Callable, 
                units="mins") -> None:
        
        """
        Functions:
        time_unit_incorporator:
            to allow for multiple time units the time_unit_incorporator function 
            returns a multiplier (lenght of time in seconds to count down)
            and the actual lenght of time to count down in seconds    
        """
        
        self.a = activity
        
        # setting the start time as a class variable, records the initialization time of class
        self.start_time = time.time()
        
        self.units = units
        self.multiplier = self.units_decoder()
        
        self.allocated_time = self.get_allocated_time()
        self.used_time = self.get_used_time()
        self.time_left = self.calculate_time_left()



    # to decode the units into a multiplier
    def units_decoder(self):
        
        if self.units == 'mins':
            multiplier = 60
        else:
            multiplier = 1
        
        return multiplier
    
    ###### Gets values from the activity db ######        
    
    def get_allocated_time(self) -> int:
        self.a.set_reset_value()
        return int(self.a.v["time_allocated"])
    
    def get_used_time(self) -> int:
        self.a.set_reset_value()
        return int(self.a.v["time_used"])
    
    def calculate_time_left(self) -> int:
        return (self.get_allocated_time() - self.get_used_time())
    
    ##########################################        

    def write_used_time_to_activity(self, used_time_in_mins_in_current_epoch: int):
        
        total_used_time = self.used_time + used_time_in_mins_in_current_epoch
        
        self.a.query.q_activity_update_time_used(total_used_time)
        
        pass

    def time_normalizer(self, time_val: int):
        return time_val//self.multiplier


    def run_timer(self):
        
        # initialize parameters
        start_time = time.time()
        time_passed_in_secs = 0
        
        # set activity status to active
        self.a.set_status(status='ACTIVE')
        
        # this is for formatting, because we are using the ansi sequence for line-up and line-clear
        print('\n\n')
        
        while self.get_used_time() < self.get_allocated_time():
            
            try:
                # seconds in an int type 
                time_passed_in_secs = round(time.time() - start_time)
                
                # print time passed to stdio
                self.time_printer(time_passed_in_secs)
                
                # pauses the function execution 
                time.sleep(self.multiplier)
            
            except KeyboardInterrupt:
                
                print("\n ----- Exitting Timer ------\n")
                cprint(f"{self.time_normalizer(time_passed_in_secs)} of {self.time_left} {self.units} done.", 
                       color="grey",
                       on_color='on_white',
                       end = '\n')
                print("-"*28)
                return
            
        # do a final write so that the completed values are recorded
        self.write_used_time_to_activity(
            used_time_in_mins_in_current_epoch=self.time_normalizer(time_passed_in_secs)
            )
        
        cprint("Timer complete. Playing alarm.", color='red')
        self.play_alarm()



    
    def time_printer(self, time_passed_in_secs: int, turbulent_time:int = 10):
        
        # these are ansi sequences to help move cursor around
        LINE_UP = '\033[1A'
        LINE_CLEAR = '\x1b[2K'
        
        time_passed_in_mins = self.time_normalizer(time_passed_in_secs)
        # print x time in mins has passed of time left
        if time_passed_in_mins < turbulent_time:
            
            cprint(f"{LINE_UP} {LINE_UP} {LINE_CLEAR} *** Turbluence, hold steady *** ", 
                   color='white',
                   on_color='on_red', 
                   end = '\n')
            
            cprint(f"{LINE_CLEAR}{self.time_left - time_passed_in_mins} left of {self.time_left} {self.units}.",
                   color = 'red'
                   )
            
            #print(LINE_UP, end = LINE_CLEAR)    
        else:
            cprint(f"{LINE_UP} {LINE_UP} {LINE_CLEAR} ~~~~ Smooth sailing ~~~~ ",
                   color='white',
                   on_color='on_green',
                   end = '\n')
            
            cprint(f"{LINE_CLEAR}{self.time_left - time_passed_in_mins} left of {self.time_left} {self.units}.",
                   color = 'yellow'
                   )
        
        # write new time_used to db
        self.write_used_time_to_activity(used_time_in_mins_in_current_epoch = time_passed_in_mins)

    def play_alarm(self):
        try:
            song = AudioSegment.from_mp3("src/roosters.mp3")
            print("playing alarm")
            play(song)
        except KeyboardInterrupt:
            print("Ending the alarm.")



if __name__ == "__main__":
    t = Timer(debug=True)
