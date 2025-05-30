import sqlite3
from datetime import datetime


class DataBase:
    def __init__(self, db_name='coffeeshop.db'):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        with self.get_connection() as conn:
            conn.execute("""
                                 CREATE TABLE IF NOT EXISTS coffeeshop (
                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 check_number INTEGER NOT NULL,
                                 operation TEXT NOT NULL,
                                 type_coffee TEXT NOT NULL,
                                 total_sum INTEGER,
                                 count_cups INTEGER NOT NULL,
                                 timestamp TEXT NOT NULL);
                        """)
            conn.commit()

    def get_connection(self):
        return sqlite3.connect(self.db_name)
        
    def add_entry(self, check_number, operation, type_coffee, count_cups, total_sum=None):
        timestamp = datetime.now().replace(microsecond=0)

        with self.get_connection() as conn:       
            conn.execute(
                """
                INSERT INTO coffeeshop (check_number, operation, type_coffee, total_sum, count_cups, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (check_number, operation, type_coffee, total_sum, count_cups, timestamp))
            conn.commit()

    def show_table(self, select_col, to_sort, **kwargs):  
        with self.get_connection() as conn: 
            if select_col or kwargs:
                cursor = self.select_by_column(select_col, conn, to_sort, **kwargs)
            else:
                sql = "SELECT * FROM coffeeshop"
                if to_sort:
                    sql += ' ORDER BY ' + ', '.join(to_sort)
                cursor = conn.execute(sql)
            return cursor.fetchall()
    
    def select_by_column(self, select_col, conn, to_sort, **kwargs):
        select = ', '.join(select_col) if select_col else '*'
        where_clauses = []
        params = []
        
        for key, values in kwargs.items():
            if isinstance(values, (tuple, list)):
                placeholders = ', '.join(['?'] * len(values))
                where_clauses.append(f"{key} IN ({placeholders})")
                params.extend(values)
            else:
                where_clauses.append(f"{key} = ?")
                params.append(values)
        
        where = ' AND '.join(where_clauses) if where_clauses else '1=1'
        sql = f"SELECT {select} FROM coffeeshop WHERE {where}"
        if to_sort:
            sql += ' ORDER BY ' + ', '.join(to_sort)
        cursor = conn.execute(sql, tuple(params))
        return cursor


    # Посчитать сумму чеков и отдельно количество чашек, за определенный период
    def sumchecks_and_countcups(self, dt_from, dt_before):
        with self.get_connection() as conn:
            conn.execute(
                """
                SELECT SUM(total_sum) as sum_of_checks, SUM(count_cups) as sum_of_cups
                FROM coffeeshop
                WHERE timestamp BETWEEN ? AND ?;
                """, (dt_from, dt_before)
                )
            cursor = conn.cursor()
            return cursor.fetchall()
        
    def update_table(self, col_name, new_val, **kwargs):
        with self.get_connection() as conn: 
            where_clauses = []
            params = []
            
            for key, values in kwargs.items():
                if isinstance(values, (tuple, list)):
                    placeholders = ', '.join(['?'] * len(values))
                    where_clauses.append(f"{key} IN ({placeholders})")
                    params.extend(values)
                else:
                    where_clauses.append(f"{key} = ?")
                    params.append(values)

            where = ' AND '.join(where_clauses) if where_clauses else '1=1'
            sql = f"UPDATE coffeeshop SET {col_name} = ? WHERE {where}"
            cursor = conn.execute(sql, (new_val, *params))
            return cursor

    def delete_from_db(self, **kwargs):
        with self.get_connection() as conn:
            if not kwargs:
                cursor = conn.execute(f"DELETE FROM coffeeshop")
            else:
                where_clauses = []
                params = []
                
                for key, values in kwargs.items():
                    if isinstance(values, (tuple, list)):
                        placeholders = ', '.join(['?'] * len(values))
                        where_clauses.append(f"{key} IN ({placeholders})")
                        params.extend(values)
                    else:
                        where_clauses.append(f"{key} = ?")
                        params.append(values)

                where = ' AND '.join(where_clauses) if where_clauses else '1=1'
                sql = f"DELETE FROM coffeeshop WHERE {where}"
                cursor = conn.execute(sql, tuple(params))
            return cursor 