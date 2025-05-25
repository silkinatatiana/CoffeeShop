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
                                 operation TEXT NOT NULL,
                                 type_coffee TEXT NOT NULL,
                                 sum INTEGER,
                                 count INTEGER NOT NULL,
                                 timestamp TEXT NOT NULL);
                        """)
            conn.commit()

    def get_connection(self):
        return sqlite3.connect(self.db_name)
        
    def add_entry(self, operation, type_coffee, count, timestamp, summa=None):
        with self.get_connection() as conn:       
            conn.execute(
                """
                INSERT INTO coffeeshop (operation, type_coffee, count, timestamp, sum)
                VALUES (?, ?, ?, ?, ?)
                """, (operation, type_coffee, count, timestamp, summa))
            conn.commit()


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
            placeholders = ', '.join(['?'] * len(args))

            conn.execute(
                f"""
                DELETE FROM coffeeshop WHERE LOWER(type_coffee)
                IN ({placeholders});
                """, 
                (args[0],)
            )
            conn.commit()

    # Удалить по типу операций
    def del_by_operation_type(self, operation_type):
        if operation_type not in ('order_coffee', 'replenish_warehouse'):
            raise ValueError("Неизвестная операция")
        
        with self.get_connection() as conn:
            conn.execute(
                """
                DELETE FROM coffeeshop WHERE operation = ?;
                """, (operation_type,)
            )
            conn.commit()

    # Сортировка по количеству, времени (одна сортировка)
    def sort_by_count_time(self):
        with self.get_connection() as conn:
            conn.execute("""
                         SELECT * FROM coffeeshop
                         ORDER BY count, timestamp;
                        """)
            conn.commit()

    # Сортировка по увеличению суммы
    def sort_by_increasing_sum(self):
        with self.get_connection() as conn:
            conn.execute("""
                         SELECT * FROM coffeeshop
                         ORDER BY sum;
                         """)

            conn.commit()

    # Посчитать сумму чеков и отдельно количество чашек, за определенный период
    def sumchecks_and_countcups(self, dt_from, dt_before):
        with self.get_connection() as conn:
            conn.execute(
                """
                SELECT SUM(sum) as sum_of_checks, SUM(count) as count_of_cups
                FROM coffeeshop
                WHERE timestamp BETWEEN ? AND ?;
                """, (dt_from, dt_before)

            )
            conn.commit()

    def select_by_cups(self, cups_from, cups_before):
        with self.get_connection() as conn:
            conn.execute(
                """
                SELECT * FROM coffeeshop WHERE count BETWEEN ? AND ?;
                """, (cups_from, cups_before)
            )
            conn.commit()

    def select_by_datetime(self, dt_from, dt_before):
        with self.get_connection() as conn:
            conn.execute(
                """
                SELECT * FROM coffeeshop
                WHERE timestamp BETWEEN ? AND ?;
                """, (dt_from, dt_before)

            )
            conn.commit()
    