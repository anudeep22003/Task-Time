import sqlite3
from termcolor import cprint
from datetime import date, timedelta


class SQLHandler:
    def __init__(self, reset=False) -> None:
        self.reset = reset
        self.column_keys = self.initialize_columns()
        self.con, self.cur = self.initialize_connection()
        self.initialize_table()

    def initialize_connection(self):
        con = sqlite3.connect(
            "src/activity.db",
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )
        cur = con.cursor()
        return con, cur

    def initialize_columns(self):
        return [
            "id",
            "created_by",
            "activity",
            "time_allocated",
            "context",
            "status",
            "date",
        ]

    def execute_initialization_script(self, q: str):
        try:
            self.con.executescript(q)
            self.con.commit()
            return True
        except Exception as e:
            cprint("Failed", color="red")
            print(e)
            return False

    def execute_write_query(self, q: str, data=None):

        if data is None:
            self.cur.execute(q)
        else:
            self.cur.execute(q, data)

        self.con.commit()

        return True

    def execute_read_query(self, q):
        return self.cur.execute(q).fetchall()

    def initialize_table(self):
        if self.reset:

            drop_query = "DROP TABLE IF EXISTS activity, activity_details"
            self.execute_write_query(q=drop_query)
            self.reset = False

        initialize_query_detailed = """
                CREATE TABLE IF NOT EXISTS activity
                (

                    created_by TEXT,
                    parent_activity text,
                    activity text,
                    time_allocated real,
                    context text, 
                    status text,
                    start_time text,
                    end_time text,
                    time_actual real, 
                    time_overage real
                )
                """

        initialize_query = """
                CREATE TABLE IF NOT EXISTS activity
                (
                    id integer not null primary key,
                    created_by TEXT,
                    activity text,
                    time_allocated real,
                    context text, 
                    status text,
                    date text
                );
                
                CREATE TABLE IF NOT EXISTS activity_details (
                activity_id INTEGER NOT NULL PRIMARY KEY,
                context TEXT,
                category TEXT, 
                notes TEXT,
                time_used TEXT,
                time_difference TEXT,
                num_edits INT,
                FOREIGN KEY (activity_id)
                    REFERENCES activity (id)
                );

                
                """

        if self.execute_initialization_script(q=initialize_query):
            cprint("\n======= Succesfully created table ========= \n", color="green")
        else:
            cprint("\nxxxxxxx Creation failed. xxxxxxx\n", color="red")

    def insert_row(self, payload: list):
        insert_query = """ INSERT INTO activity 
        (created_by, activity, time_allocated, context, status, date)
        VALUES (?, ?, ?, ?, ?, ?)"""
        self.execute_write_query(q=insert_query, data=payload)

    def read_rows(self, days_offset=0, status=None, id=None, include_keys=False):

        d = date.today() + timedelta(days=days_offset)
        d = d.strftime("%Y-%m-%d")
        if status is None and id is None:

            read_query = f"""select id, activity, time_allocated, status from activity 
                    where date = "{d}"
            """
        elif status is None and id is not None:
            read_query = f"""select * from activity 
                    where date = "{d}" and id = {id}
            """

        elif status == "INCOMPLETE":
            # filter = [f"and {k} = {v}" for k,v in status.items()]
            read_query = f"""select id, activity, time_allocated, status from activity 
                    where date = "{d}" and status != "COMPLETED" 
            """

        elif status == "COMPLETED":
            # filter = [f"and {k} = {v}" for k,v in status.items()]
            read_query = f"""select id, activity, time_allocated, status from activity 
                    where date = "{d}" and status = "COMPLETED" 
            """

        else:
            read_query = f"""select * from activity 
                    where date = "{d}" and status = "COMPLETED" 
            """

        output = self.execute_read_query(q=read_query)

        if include_keys:
            return self.column_keys, output
        else:
            return output
