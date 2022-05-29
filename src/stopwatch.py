import time
from termcolor import cprint
from pydub import AudioSegment
from pydub.playback import play


class Timer:
    def __init__(
        self, length_of_time: float, start_time: time, units="seconds", debug=False
    ) -> None:
        self.start_time = start_time
        self.units = units

        self.multiplier, self.length_of_time = self.time_unit_incorporator(
            length_of_time
        )
        self.time_left = self.length_of_time

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

    def stopwatch_orchestrator(self):
        while self.time_left > 0:
            try:
                time_elapsed = round(time.time() - self.start_time, 0)
                self.time_left = self.length_of_time - time_elapsed
                cprint(
                    f"Time left: {self.time_left/self.multiplier} {self.units}",
                    end="\r",
                    color="yellow",
                )
                time.sleep(self.multiplier)
            except KeyboardInterrupt:
                # meaning timer was only partially required
                print(
                    "Exitting... \t\t Time elapsed: {} seconds".format(
                        round(time.time() - self.start_time, 0)
                    )
                )
                return float(self.time_left / self.multiplier)

        self.play_alarm()
        cprint("Timer complete.  Alarm being Played", color="red")
        # meaning the timer ran fully and exited
        return True

    def play_alarm(self):
        try:
            song = AudioSegment.from_mp3("src/roosters.mp3")
            print("playing alarm")
            play(song)
        except KeyboardInterrupt:
            print("Ending the alarm.")


if __name__ == "__main__":
    t = Timer(debug=True)
