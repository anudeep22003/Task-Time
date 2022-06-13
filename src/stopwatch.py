import time
from termcolor import cprint
from pydub import AudioSegment
from pydub.playback import play


class Timer:
    def __init__(self, length_of_time: float, start_time: time, units="seconds", debug=False) -> None:
        
        """
        Functions:
        time_unit_incorporator:
            to allow for multiple time units the time_unit_incorporator function 
            returns a multiplier (lenght of time in seconds to count down)
            and the actual lenght of time to count down in seconds    
        """
        
        self.start_time = start_time
        self.units = units

        # to allow for multiple time units the time_unit_incorporator function 
        # returns a multiplier (lenght of time in seconds to count down)
        # and the actual lenght of time to count down in seconds
        self.multiplier, self.length_of_time = self.time_unit_incorporator(length_of_time)
        
        
        if debug:
            self.stopwatch_orchestrator()

    def input_orchestrator(self):
        length_of_time = float(input("Enter how long the timer will run for:\t"))
        return length_of_time, length_of_time

    def time_unit_incorporator(self, time):
        if self.units == "mins":
            return 60, time * 60
        if self.units == "hours":
            return 60, time * 60 * 60
        else:
            return 1, time

    def time_printer(self, elapsed_time: time, total_time: time, multiplier: int = 60, turbulence: float = 0.1):
        time_left = (total_time - elapsed_time)/multiplier
        elapsed_time = elapsed_time/multiplier
        
        total_time = total_time/multiplier
        turbulent_time = total_time * turbulence
        if elapsed_time > turbulent_time and elapsed_time>10:
            cprint(f""" Smooth sailing: {time_left} left of {total_time} mins""", color = 'yellow', end = '\r')
        else:
            cprint(f""" Turbulent: {time_left} left of {total_time} mins""", color = 'red', on_color='on_yellow', end = '\r')

    
    
    def stopwatch_orchestrator(self):
        
        time_elapsed = time.time() - self.start_time
        # while the timer has not run out, continue in the loop
        
        while self.length_of_time > time_elapsed:
            try:
                # a temp variable I am using to keep track of how much time has elapsed in the timer
                time_elapsed = round(time.time() - self.start_time, 0)
                
                self.time_printer(time_elapsed, self.length_of_time, self.multiplier)
                
                # cprint(
                #     f"Time left: {(self.length_of_time - time_elapsed)/self.multiplier} {self.units}",
                #     end="\r",
                #     color="yellow",
                # )
                time.sleep(self.multiplier)
            except KeyboardInterrupt:
                # meaning timer was only partially required
                print(
                    "Exitting... \t\t Time elapsed: {} seconds".format(
                        round(time_elapsed, 0)
                    )
                )
                return int(time_elapsed / self.multiplier)

        self.play_alarm()
        cprint("Timer complete.  Alarm being Played", color="red")
        # meaning the timer ran fully and exited
        return int(time_elapsed/self.multiplier)

    def play_alarm(self):
        try:
            song = AudioSegment.from_mp3("src/roosters.mp3")
            print("playing alarm")
            play(song)
        except KeyboardInterrupt:
            print("Ending the alarm.")


if __name__ == "__main__":
    t = Timer(debug=True)
