from dataclasses import dataclass
from datetime import date, timedelta
from db_interface import SQLHandler
from pprint import pprint
from termcolor import cprint

from query_factory import SqlQueryFactory


class ActivityInterfacer:
    def __init__(self) -> None:
        self.sql = SQLHandler()
        pass

    def create_activity():
        pass

    def activity_register():
        pass

    def activity_editor():
        pass

    def activity_deletor():
        pass

    def load_activity():
        pass

    def show_today_activities():
        today = date.today()
        # fetch today's tasks
        pass

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

            row.extend(
                [created_by, activity, allocated_time, "", status, activity_date]
            )

            self.sql.insert_row(payload=row)

    def start_day(self):
        print(
            "{:^10s}\t{:^10s}\t{:<10s}\t{:<20s}".format(
                "id", "time", "status", "activity"
            )
        )
        print("{:*^10s}\t{:*^10s}\t{:*<10s}\t{:*<20s}".format("", "", "", ""))
        for row in self.sql.read_rows(status="INCOMPLETE"):
            id, activity, time, status = row
            print(
                "{:^10s}\t{:^10s}\t{:<10s}\t{:<20s}".format(
                    str(id), str(time), status, activity
                )
            )

    def lookback(self):
        print(
            "{:^10s}\t{:^10s}\t{:<10s}\t{:<20s}".format(
                "id", "time", "status", "activity"
            )
        )
        print("{:*^10s}\t{:*^10s}\t{:*<10s}\t{:*<20s}".format("", "", "", ""))
        for row in self.sql.read_rows(status="COMPLETED"):
            id, activity, time, status = row
            print(
                "{:^10s}\t{:^10s}\t{:<10s}\t{:<20s}".format(
                    str(id), str(time), status, activity
                )
            )
        pass

    def instantiate_activity(self, id: int):
        # print("entered here")
        activity_payload = self.retreive_activity(id)
        return Activity(activity_payload)

    def retreive_activity(self, id):
        keys, output = self.sql.read_rows(id=id, include_keys=True)
        # print(keys)
        # print(output)

        # pprint(dict(zip(keys,output)))
        # print("exited here")
        return dict(zip(keys, output[0]))


@dataclass
class Activity:
    def __init__(self, row: dict) -> None:
        self.id = row["id"]
        self.created_by = row["created_by"]
        self.activity = row["activity"]
        self.time_allocated = row["time_allocated"]
        self.context = row["context"]
        self.status = row["status"]
        self.date = row["date"]

        self.sql = SQLHandler()
        self.query = SqlQueryFactory()
        pass

    def activity_update(self, status="RUNNING"):

        q = f"""
            Update activity
            set status = "{status}"
            where id = {self.id}
        """
        self.sql.execute_write_query(q)

        self.status = status

    def activity_edit(self):
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
            new_activity = self.activity
        if new_time == "":
            new_time = self.time_allocated

        # run an update query and inform on status of completion
        if self.query.q_activity_edit(self.id, new_activity, new_time):
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
                    self.id,
                    self.activity,
                    updated_time=self.time_allocated + extra_time,
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
                if self.query.q_status_update(self.id, status=user_set_status):
                    cprint(f"status updated to {user_set_status}", color="green")
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
                if self.query.q_status_update(self.id, status[choice]):
                    cprint(f"status updated to {status[choice]}", color="green")
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
                if self.query.q_date_update(self.id, days_in_future):
                    cprint(
                        f"Rescheduled to #{days_in_future} days in the future",
                        color="green",
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
                cprint(f"Current status\t--> {self.status}", color="yellow")
                self.set_status()

            elif choice == "t":
                self.update_time()

            elif choice == "c":
                # add context
                print("TODO: option not yet added")
                self.add_context()
                pass

            elif choice == "d":
                cprint("Duplicating to tomorrow, but not really", color="red")
                return "Something to trigger func call"

            # mark status

            # request extra time

            # add context / notes

            # copy to tomorrow

            pass

    def show_feedback(self):
        keys = ["#Activities", "Total time", "Average time"]
        response = self.query.q_sum_of_time(date=self.date)
        for r in response:
            for k, v in zip(keys, r):
                cprint(f"{k}: {v}\t", end="", color="green")
            print("\n")

    def add_context(self):
        while True:
            valid_options = ["c", "a", "x"]

            # add context or notes
            cprint("(c) Add context\t (n) Add notes\t (x) Exit", color="yellow")
            choice = input("Enter choice\t--> ")
            if choice not in valid_options:
                cprint("Invalid choice; try again", color="red")
            elif choice == "x":
                break
            elif choice == "c":
                # add context
                cprint("\nEnter the context here", color="yellow")
                user_input_context = input("Enter here\t--> ")
                self.query.q_update_context(id=self.id, context=user_input_context)

            elif choice == "n":
                # add a note
                cprint("\nEnter the notes here", color="yellow")
                note = input("Enter here\t--> ")
                pass

        pass

    pass
