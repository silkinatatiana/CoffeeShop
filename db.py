import sqlite3
from datetime import datetime


class DataBase:
    def __init__(self):
        self.db_coffee = 'coffee.db'
        self.db_coffeeshop = 'sales.db'
        self.db_warehouse = 'warehouse.db'
        self.create_table_coffee()
        self.create_table_sales()
        self.create_table_warehouse()

    def create_table_coffee(self):
        with self.get_connection('coffee.db') as conn:
            conn.execute("""
                        CREATE TABLE IF NOT EXISTS coffee (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        type_coffee TEXT NOT NULL,
                        price INTEGER,
                        check_number INTEGER
                        invoice INTEGER);
                        """)
            conn.commit()

    def create_table_sales(self):
        with self.get_connection('sales.db') as conn:
            conn.execute("""
                        CREATE TABLE IF NOT EXISTS sales (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        check_number INTEGER NOT NULL,
                        count_cups INTEGER NOT NULL,
                        total_sum INTEGER,
                        timestamp TEXT NOT NULL);
                        """)
            conn.commit()

    def create_table_warehouse(self):
        with self.get_connection('warehouse.db') as conn:
            conn.execute("""
                        CREATE TABLE IF NOT EXISTS warehouse (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        type_coffee TEXT NOT NULL,
                        count_cups INTEGER NOT NULL,
                        invoice INTEGER NOT NULL);
                        """)
            conn.commit()

    def get_connection(self, db_name):
        return sqlite3.connect(db_name)
        
    def add_entry_coffee(self, type_coffee, price, check_number=None, invoice=None):
        with self.get_connection('coffee.db') as conn:       
            conn.execute(
                """
                INSERT INTO coffee.db (type_coffee, price, check_number, invoice)
                VALUES (?, ?, ?, ?)
                """, (type_coffee, price, check_number, invoice))
            conn.commit()

    def add_entry_sales(self, check_number, count_cups, total_sum):
        timestamp = datetime.now().replace(microsecond=0)
        
        with self.get_connection('sales.db') as conn:       
            conn.execute(
                """
                INSERT INTO sales.db (check_number, count_cups, total_sum, timestamp)
                VALUES (?, ?, ?, ?)
                """, (check_number, count_cups, total_sum, timestamp))
            conn.commit()

    def add_entry_warehouse(self, type_coffee, count_cups, invoice):        
        with self.get_connection('warehouse.db') as conn:       
            conn.execute(
                """
                INSERT INTO warehouse.db (type_coffee, count_cups, invoice)
                VALUES (?, ?, ?)
                """, (type_coffee, count_cups, invoice))
            conn.commit()

    def check_nametable(self, table_name):
        if table_name not in ('coffee', 'sales', 'warehouse'):
            raise Exception ("Базы данных не существует")

    def show_table(self, table_name, *args):
        self.check_nametable(table_name)
        if len(args) == 0:
            sql = "SELECT * FROM ?;"
        else:
            sql = "SELECT * FROM ? WHERE operation = ?;"
        with self.get_connection(table_name + '.db') as conn:
            conn.execute(sql, (table_name, args[0]))

            cursor = conn.cursor()
            return cursor.fetchall()

    def select_by_cups(self, cups_from, cups_before):

        with self.get_connection('sales.db') as conn:
            conn.execute(
                """
                SELECT * FROM sales WHERE count_cups BETWEEN ? AND ?;
                """, (cups_from, cups_before)
            )
            cursor = conn.cursor()
            return cursor.fetchall()

    def select_by_datetime(self, dt_from, dt_before):
        with self.get_connection('sales.db') as conn:
            conn.execute(
                """
                SELECT * FROM sales
                WHERE timestamp BETWEEN ? AND ?;
                """, (dt_from, dt_before)
            )
            cursor = conn.cursor()
            return cursor.fetchall()
        
    # Сортировка по количеству, времени (одна сортировка)
    def sort_by_count_time(self):
        with self.get_connection('sales.db') as conn:
            conn.execute("""
                         SELECT * FROM sales
                         ORDER BY count_cups, timestamp;
                        """)
            
            cursor = conn.cursor()
            return cursor.fetchall()

    # Сортировка по увеличению суммы
    def sort_by_increasing_sum(self):
        with self.get_connection('sales.db') as conn:
            conn.execute("""
                         SELECT * FROM sales
                         ORDER BY total_sum;
                         """)

            cursor = conn.cursor()
            return cursor.fetchall()

    # Посчитать сумму чеков и отдельно количество чашек, за определенный период
    def sumchecks_and_countcups(self, dt_from, dt_before):
        with self.get_connection('sales.db') as conn:
            conn.execute(
                """
                SELECT SUM(total_sum) as sum_of_checks, SUM(count_cups) as sum_of_cups
                FROM sales
                WHERE timestamp BETWEEN ? AND ?;
                """, (dt_from, dt_before)
                )
            cursor = conn.cursor()
            return cursor.fetchall()
        
    # Удаление записи из БД до указанного времени datetime
    def del_before_time(self, dt):
        with self.get_connection('sales.db') as conn:
            conn.execute(
                """
                DELETE FROM sales
                WHERE timestamp < ?;
                """, (dt,)
            )
            conn.commit()

    # # Удалить записи где был куплен определенный вид кофе
    # def del_by_coffee_type(self, *args):
    #     if not args:
    #         raise ValueError("Необходимо указать хотя бы один тип кофе")
        
    #     with self.get_connection('sales.db') as conn:
    #         with self.get_connection('coffee.db') as conn2:
                
    #             conditions = " OR ".join(["type_coffee LIKE ?" for _ in args])
    #             params = [f"%{coffee_type}%" for coffee_type in args]
                
    #             conn.execute(
    #                 f"""
    #                 DELETE FROM coffeeshop 
    #                 WHERE {conditions};
    #                 """, 
    #                 params
    #             )
    #             conn.commit()



