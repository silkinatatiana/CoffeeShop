import sqlite3
from datetime import datetime


class DataBase:
    def __init__(self, db_name='coffeeshop', table_sales=None, table_warehouse=None, stock=None):
        self.db_name = db_name
        self.table_sales = table_sales
        self.table_warehouse = table_warehouse
        self.stock = stock      

        with self.get_connection() as conn:
            sql_tables = []

            if self.table_sales:
                sql_tables.append(self.sql_request('sales'))
            if self.table_warehouse:    
               sql_tables.append(self.sql_request('warehouse'))
            if self.stock:
                sql_tables.append(self.sql_request('stock'))

            for sql in sql_tables:
                conn.execute(sql)
            conn.commit()

    def sql_request(self, table):
            match table:
                case 'sales':
                    sql = """
                        CREATE TABLE IF NOT EXISTS sales (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        check_number INTEGER,
                        type_coffee TEXT NOT NULL,
                        count_cups INTEGER NOT NULL,
                        price INTEGER NOT NULL,
                        timestamp TEXT NOT NULL);
                        """
                case 'warehouse':
                    sql = """
                        CREATE TABLE IF NOT EXISTS warehouse (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        invoice INTEGER,
                        type_coffee TEXT NOT NULL,
                        count_cups INTEGER NOT NULL,
                        purchase_cost INTEGER NOT NULL,
                        timestamp TEXT NOT NULL);
                        """
                case 'stock':
                    sql = """
                          CREATE TABLE IF NOT EXISTS stock (
                          type_coffee TEXT PRIMARY KEY,
                          count_cups INTEGER NOT NULL DEFAULT 0);
                        """
                case _:
                    raise NameError("Неизвестная база таблица")
            return sql

    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def get_current_stock(self, coffee_name: str) -> int:
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT count_cups FROM stock WHERE type_coffee = ?", (coffee_name,))
            result = cursor.fetchone()
            return result[0] if result else 0

    def update_stock(self, coffee_name, delta_quantity, add):
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT count_cups FROM stock WHERE type_coffee = ?",
                (coffee_name,)
            )
            record = cursor.fetchone()

            if record is None:
                new_quantity = delta_quantity if add else -delta_quantity
                conn.execute(
                    "INSERT INTO stock (type_coffee, count_cups) VALUES (?, ?)",
                    (coffee_name, max(new_quantity, 0))
                )
            else:
                current = record[0]
                new_quantity = current + delta_quantity if add else current - delta_quantity
                conn.execute(
                    "UPDATE stock SET count_cups = ? WHERE type_coffee = ?",
                    (max(new_quantity, 0), coffee_name)
                )
            conn.commit()
        
    def add_entry_sales(self, check_number, type_coffee, count_cups, price):
        timestamp = datetime.now().replace(microsecond=0)
        with self.get_connection() as conn:       
            conn.execute(
                """
                INSERT INTO sales (check_number, type_coffee, count_cups, price, timestamp)
                VALUES (?, ?, ?, ?, ?)
                """, (check_number, type_coffee, count_cups, price, timestamp))
            conn.commit()

    def add_entry_warehouse(self, invoice, type_coffee, count_cups, purchase_cost):    
        timestamp = datetime.now().replace(microsecond=0)

        with self.get_connection() as conn:       
            conn.execute(
                """
                INSERT INTO warehouse (invoice, type_coffee, count_cups, purchase_cost, timestamp)
                VALUES (?, ?, ?, ?, ?)
                """, (invoice, type_coffee, count_cups, purchase_cost, timestamp))
            conn.commit()
    
    def add_entry_stock(self, type_coffee, count_cups):
        with self.get_connection() as conn:       
            conn.execute(
                """
                INSERT INTO stock (type_coffee, count_cups)
                VALUES (?, ?)
                """, (type_coffee, count_cups))
            conn.commit()

    def get_last_check_number(self):
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT MAX(check_number) FROM sales;")
            result = cursor.fetchone()[0]
            return result if result is not None else None

    def get_last_invoice_number(self):
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT MAX(invoice) FROM warehouse;")
            result = cursor.fetchone()[0]
            return result if result is not None else None

    def show_table(self, table, select_col=None, to_sort=None, **kwargs):
        with self.get_connection() as conn:
            select = "*" if not select_col else ", ".join(select_col)
            
            where_clauses = []
            params = []
            
            for key, values in kwargs.items():
                if isinstance(values, (list, tuple)):
                    placeholders = ", ".join(["?"] * len(values))
                    where_clauses.append(f"{key} IN ({placeholders})")
                    params.extend(values)
                else:
                    where_clauses.append(f"{key} = ?")
                    params.append(values)
            
            sql = f"SELECT {select} FROM {table}"
            
            if where_clauses:
                sql += " WHERE " + " AND ".join(where_clauses)
            
            if to_sort:
                sql += " ORDER BY " + ", ".join(to_sort)
            
            cursor = conn.execute(sql, tuple(params))
            return cursor.fetchall()
        
    def update_table(self, table, col_name, new_val, **kwargs):
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
            sql = f"UPDATE {table} SET {col_name} = ? WHERE {where}"
            cursor = conn.execute(sql, (new_val, *params))
            return cursor

    def delete_from_db(self, table, **kwargs):
        with self.get_connection() as conn:
            if not kwargs:
                cursor = conn.execute(f"DELETE FROM {table}")
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
                sql = f"DELETE FROM {table} WHERE {where}"
                cursor = conn.execute(sql, tuple(params))
            return cursor 
        
    def sumchecks_and_countcups(self, dt_from, dt_before):
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT 
                SUM(price * count_cups) as sum_of_checks, 
                SUM(count_cups) as sum_of_cups
                FROM sales
                WHERE timestamp BETWEEN ? AND ?;
                """, (dt_from, dt_before)
                )
            return cursor.fetchall()

    def calculate_profit(self, dt_from, dt_before):
        with self.get_connection() as conn:
            sql = """
                  SELECT sales.type_coffee, 
                  SUM(sales.count_cups * sales.price) - SUM(w.count_cups * w.purchase_cost) AS profit
                  FROM sales
                  JOIN warehouse w ON sales.type_coffee = w.type_coffee
                  """
            params = []

            if dt_from and dt_before:
                sql += " WHERE sales.timestamp BETWEEN ? AND ?"
                params.extend([dt_from, dt_before])

            sql += " GROUP BY sales.type_coffee;"

            if params:
                cursor = conn.execute(sql, params)
            else:
                cursor = conn.execute(sql)
                
            return cursor.fetchall()
  
    def check_information(self):
        with self.get_connection() as conn:
            cursor = conn.execute("""
                                  SELECT check_number, type_coffee, SUM(price) AS total_check
                                  FROM sales
                                  GROUP BY check_number
                                  ORDER BY check_number;""") 
            return cursor.fetchall()   
        
    def all_info(self):
        with self.get_connection() as conn:
            cursor = conn.execute("""
                    SELECT s.type_coffee, SUM(s.count_cups) AS sold_cups,
                       (SELECT SUM(w.count_cups) FROM warehouse w WHERE w.type_coffee = s.type_coffee) AS purchased_cups,
                       (SELECT SUM(st.count_cups) FROM stock st WHERE st.type_coffee = s.type_coffee) AS remainder
                FROM sales s
                GROUP BY s.type_coffee;
                    """)
            return cursor.fetchall() 
