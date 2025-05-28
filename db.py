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

    def show_table(self, *args):
        if len(args) == 0:
            sql = "SELECT * FROM coffeeshop;"
            params = ()
        else:
            sql = "SELECT * FROM coffeeshop WHERE operation = ?;"
            params = (args[0],)
            
        with self.get_connection() as conn:
            cursor = conn.execute(sql, params)
            return cursor.fetchall()



    def select_by_cups(self, cups_from, cups_before):
        with self.get_connection() as conn:
            conn.execute(
                """
                SELECT * FROM coffeeshop WHERE count_cups BETWEEN ? AND ?;
                """, (cups_from, cups_before)
            )
            cursor = conn.cursor()
            return cursor.fetchall()

    def select_by_datetime(self, dt_from, dt_before):
        with self.get_connection() as conn:
            conn.execute(
                """
                SELECT * FROM coffeeshop
                WHERE timestamp BETWEEN ? AND ?;
                """, (dt_from, dt_before)
            )
            cursor = conn.cursor()
            return cursor.fetchall()
        
    # Сортировка по количеству, времени (одна сортировка)
    def sort_by_count_time(self):
        with self.get_connection() as conn:
            conn.execute("""
                         SELECT * FROM coffeeshop
                         ORDER BY count_cups, timestamp;
                        """)
            
            cursor = conn.cursor()
            return cursor.fetchall()

    # Сортировка по увеличению суммы
    def sort_by_increasing_sum(self):
        with self.get_connection() as conn:
            conn.execute("""
                         SELECT * FROM coffeeshop
                         ORDER BY total_sum;
                         """)

            cursor = conn.cursor()
            return cursor.fetchall()

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
        
        # Удаление записи из БД до указанного времени datetime
    def del_before_time(self, dt):
        with self.get_connection() as conn:
            conn.execute(
                """
                DELETE FROM coffeeshop
                WHERE timestamp < ?;
                """, (dt,)
            )
            conn.commit()

    # Удалить записи где был куплен определенный вид кофе
    def del_by_coffee_type(self, *args):
        if not args:
            raise ValueError("Необходимо указать хотя бы один тип кофе")
        
        with self.get_connection() as conn:
            conditions = " OR ".join(["type_coffee LIKE ?" for _ in args])
            params = [f"%{coffee_type}%" for coffee_type in args]
            
            conn.execute(
                f"""
                DELETE FROM coffeeshop 
                WHERE {conditions};
                """, 
                params
            )
            conn.commit()

    # Удалить по типу операций
    def del_by_operation_type(self, operation_type):
        if operation_type not in ('заказ кофе', 'пополнение склада'):
            raise ValueError("Неизвестная операция")
        
        with self.get_connection() as conn:
            conn.execute(
                """
                DELETE FROM coffeeshop WHERE operation = ?;
                """, (operation_type,)
            )
            conn.commit()
