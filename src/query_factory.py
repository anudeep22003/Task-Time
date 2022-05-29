import sqlite3
from datetime import date, timedelta


class SqlQueryFactory:
    def __init__(self) -> None:
        self.sql = SqlQueryExecutor()
        pass

    def q_activity_edit(self, id: int, updated_activity: str, updated_time: str):
        q = f""" 
    UPDATE activity
    SET activity = "{updated_activity}", time_allocated = "{updated_time}"
    WHERE id = {id}
    """
        return self.sql.execute_write_query(q)

    def q_status_update(self, id: int, status: str):
        q = f"""UPDATE activity 
        SET status = "{status}"
        WHERE id = {id}
        """
        return self.sql.execute_write_query(q)

    def q_date_update(self, id: int, days_offset: int):

        d = date.today() + timedelta(days=days_offset)
        d = d.strftime("%Y-%m-%d")

        q = f"""UPDATE activity 
        SET date = "{d}"
        WHERE id = {id}
        """

        return self.sql.execute_write_query(q)

    def q_update_context(self, id, context):

        q = f"""Insert into activity_details 
        (activity_id, context, notes)
        VALUES ({id}, "{context}","")
        ON DUPLICATE KEY 
            UPDATE context = context || ". {context}"
        """

        return self.sql.execute_write_query(q)

    def q_sum_of_time(self, date: str, status: str = "COMPLETED"):
        q = f"""Select 
            COUNT(*) as num_activities, 
            SUM(time_allocated) as time,
            AVG(time_allocated) as average
            from activity
            where date = "{date}" and status = "{status}"
                
                """
        return self.sql.execute_read_query(q)

    def q_insert_row(self):
        return """ INSERT INTO activity 
        (created_by, activity, time_allocated, context, status, date)
        VALUES (?, ?, ?, ?, ?, ?)"""


class SqlQueryExecutor:
    def __init__(self) -> None:
        self.con, self.cur = self.initialize_connection()

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

    def execute_write_query(self, q: str, data=None):
        try:
            if data is None:
                self.cur.execute(q)
            else:
                self.cur.execute(q, data)

            self.con.commit()
            return True

        except Exception as e:
            print(e)
            return False

    def execute_read_query(self, q):
        return self.cur.execute(q).fetchall()
