import sqlite3
from termcolor import cprint


class SQLHandler:
    def __init__(self, reset=False) -> None:
        self.reset = reset
        self.con, self.cur = self.initialize_connection()
        self.initialize_table()

    def initialize_connection(self):
        con = sqlite3.connect(
            "src/activity.db",
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )
        cur = con.cursor()
        return con, cur


    def execute_initialization_script(self, q: str):
        try:
            self.con.executescript(q)
            self.con.commit()
            return True
        except Exception as e:
            cprint("Failed", color="red")
            print(e)
            return False


    def initialize_table(self):
        if self.reset:

            drop_query = """DROP TABLE IF EXISTS activity;
            DROP TABLE IF EXISTS activity_details;
            """
        else:
            drop_query = ""
            # self.execute_write_query(q=drop_query)
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

        initialize_query = f"""
                {drop_query}
        
                CREATE TABLE IF NOT EXISTS activity
                (
                    id integer not null primary key,
                    created_by TEXT,
                    activity text,
                    time_allocated real,
                    context text, 
                    status text,
                    date text,
                    time_used text
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

if __name__ == "__main__":
    s = SQLHandler(reset=True)