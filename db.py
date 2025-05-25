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
