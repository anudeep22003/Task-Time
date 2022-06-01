import sqlite3
from datetime import date, timedelta
from xml.etree.ElementInclude import include
from xmlrpc.client import Boolean


class SqlActivityQueryFactory:
    
    def __init__(self, id: int) -> None:
        self.sql = SqlQueryExecutor()
        self.id = id
        pass

    def q_activity_update_time_used(self, time_used:int):
        q = f"""Update activity
        set time_used = {time_used}
        where id = {self.id}
        """
        
        return self.sql.execute_write_query(q)
    
    def q_activity_edit(self, updated_activity: str, updated_time: str):
        q = f""" 
        UPDATE activity
        SET activity = "{updated_activity}", time_allocated = "{updated_time}"
        WHERE id = {self.id}
        """
        return self.sql.execute_write_query(q)

    def q_activity_status_update(self, status: str):
        q = f"""UPDATE activity 
        SET status = "{status}"
        WHERE id = {self.id}
        """
        return self.sql.execute_write_query(q)

    def q_activity_date_update(self, days_offset: int):

        d = date.today() + timedelta(days=days_offset)
        d = d.strftime("%Y-%m-%d")

        q = f"""UPDATE activity 
        SET date = "{d}"
        WHERE id = {self.id}
        """

        return self.sql.execute_write_query(q)

    def q_activity_update_context(self, context):

        q = f"""Insert into activity_details 
        (activity_id, context, notes)
        VALUES ({self.id}, "{context}","")
        ON DUPLICATE KEY 
            UPDATE context = context || ". {context}"
        """

        return self.sql.execute_write_query(q)
        

class SqlGeneralQueryFactory:
    def __init__(self) -> None:
        self.sql = SqlQueryExecutor()
        pass
    
    def get_column_keys(self):
        return [
            "id",
            "created_by",
            "activity",
            "time_allocated",
            "context",
            "status",
            "date",
            "time_used"
        ]
        
    def q_delete_activity(self, id: int):
        q = f"DELETE FROM activity WHERE id = {id}"
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

    def q_insert_row(self,payload:list):
        q = """ INSERT INTO activity 
        (created_by, activity, time_allocated, context, status, date, time_used)
        VALUES (?, ?, ?, ?, ?, ?, ?)"""
        return self.sql.execute_write_query(q,payload)

    def date_to_string_converter(self, date_input: date = date.today(), days_offset: int = 0):
        d = date_input + timedelta(days=days_offset)
        return d.strftime("%Y-%m-%d")
            
    
    def read_today_rows(self, days_offset:int = 0):
        d = self.date_to_string_converter(days_offset=days_offset)
        q = f"""select id, activity, time_allocated, status from activity 
                    where date = "{d}"
            """
        return self.sql.execute_read_query(q)
    
    def return_activity_row(self, id:int, include_keys: bool = False):
        q = f"""select * from activity 
                    where id = {id}
            """
        if include_keys:
            return self.get_column_keys(), self.sql.execute_read_query(q) 
        else:
            return self.sql.execute_read_query(q)
    
    def read_rows_by_status(self, status:str, days_offset:int = 0):
        
        d = self.date_to_string_converter(days_offset=days_offset)
        
        if status == "INCOMPLETE":
            # filter = [f"and {k} = {v}" for k,v in status.items()]
            q = f"""select id, activity, time_allocated, status, time_used from activity 
                    where date = "{d}" and status != "COMPLETED" 
            """

        elif status == "COMPLETED":
            # filter = [f"and {k} = {v}" for k,v in status.items()]
            q = f"""select id, activity, time_allocated, status, time_used from activity 
                    where date = "{d}" and status = "COMPLETED" 
            """
        return self.sql.execute_read_query(q)
    

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
