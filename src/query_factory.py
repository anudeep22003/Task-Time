from multiprocessing import context
import sqlite3
from datetime import date, timedelta


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
    
    def q_activity_add_time_used(self, incremental_time_used:int):
        q = f"""UPDATE activity
        SET time_used = time_used + {incremental_time_used}
        WHERE id = {self.id}
        """
        
        return self.sql.execute_write_query(q)


    def q_add_time(self, extra_time: int = 0):
        q = f"""
            UPDATE activity
            SET time_allocated = time_allocated + {extra_time}
            WHERE id = {self.id}
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


class SqlActivityDetailsQueryFactory:

    def __init__(self, parent_activity_id: int) -> None:
        self.id = parent_activity_id
        self.sql = SqlQueryExecutor()
        
        # initialize the row 
        self.initialize_details()
        pass
    
    def initialize_details(self):
        q = f""" INSERT OR IGNORE INTO activity_details (activity_id, context, notes, num_edits)
        VALUES({self.id},"","", 0)
        """
        self.sql.execute_write_query(q)
        pass
    
    def initialize_daughter_details(self, context: str, notes:str= ""):
        
        if context:
            self.q_add_context(context)
            self.q_add_separator(field='context')
        
        if notes:
            self.q_add_notes(notes)
            self.q_add_separator(field='notes')

        
        pass
    
    def q_add_separator(self, field: str = "context"):
        separator = f'----------- Above added on {date.today().strftime("%d-%b-%y")} --------------'
        
        q = f""" 
        
        UPDATE activity_details
        SET 
        {field} = {field} || char(10) ||  char(10) || "{separator}"
        
        WHERE
        activity_id = {self.id}
        """
        
        self.sql.execute_write_query(q)
    
    
    def q_add_context(self, context: str):
        
        q = f""" 
        
        UPDATE activity_details
        SET 
        context = context || char(10) || "{context}" 
        
        WHERE
        activity_id = {self.id}
        """
        
        self.sql.execute_write_query(q)
        pass
    
    def q_add_notes(self, notes:str):
        
        q = f"""
        UPDATE activity_details
        SET 
        notes = notes || char(10) || "{notes}" 
        
        WHERE 
        activity_id = {self.id}
        
        """

        self.sql.execute_write_query(q)
    
    
    def show_details(self):
        q = f"""
        SELECT context, notes FROM activity_details 
        WHERE activity_id = {self.id}
        """
        return self.sql.execute_read_query(q)
    
    def get_context(self):
        q = f"""
        SELECT context FROM activity_details 
        WHERE activity_id = {self.id}
        """
        
        for row in self.sql.execute_single_read_query(q):
            context = row
        return context

    def get_notes(self):
        q = f"""
        SELECT notes FROM activity_details 
        WHERE activity_id = {self.id}
        """
        for row in self.sql.execute_single_read_query(q):
            notes = row
        return notes


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
                    ORDER BY status, time_allocated DESC
            """

        elif status == "COMPLETED":
            # filter = [f"and {k} = {v}" for k,v in status.items()]
            q = f"""select id, activity, time_allocated, status, time_used from activity 
                    where date = "{d}" and status = "COMPLETED" 
            """
        return self.sql.execute_read_query(q)
    
    def q_get_aggregate_incomplete(self, days_offset:int = 0):
        
        d = self.date_to_string_converter(days_offset=days_offset)

        q = f"""SELECT COUNT(*), SUM(time_used), SUM(time_allocated) FROM activity
                WHERE date = "{d}" and status != "COMPLETED"
                """
        
        return self.sql.execute_read_query(q)        
        
    def q_get_aggregate_complete(self, days_offset:int = 0):
        
        d = self.date_to_string_converter(days_offset=days_offset)

        q = f"""SELECT COUNT(*), SUM(time_used), SUM(time_allocated) FROM activity
                WHERE date = "{d}" and status = "COMPLETED"
                """
        
        return self.sql.execute_read_query(q)        
        
    def q_get_aggregate_all(self, days_offset:int = 0):
        
        d = self.date_to_string_converter(days_offset=days_offset)

        q = f"""SELECT COUNT(*), SUM(time_used), SUM(time_allocated) FROM activity
                WHERE date = "{d}" 
                """
        
        return self.sql.execute_read_query(q)        
        
        pass

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


    def last_row_inserted(self):
        return self.cur.lastrowid

    def execute_write_query(self, q: str, data=None):
        try:
            if data is None:
                self.cur.execute(q)
            else:
                self.cur.execute(q, data)

            self.con.commit()
            return self.last_row_inserted()

        except Exception as e:
            print(e)
            return False

    def execute_read_query(self, q):
        return self.cur.execute(q).fetchall()
    
    def execute_single_read_query(self, q):
        return self.cur.execute(q).fetchone()
