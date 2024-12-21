import sqlite3
import pandas as pd


class DatabaseHandler:
    def __init__(self, db_name="childcare.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS childcare_data (
                                id INTEGER PRIMARY KEY,
                                full_day_fee REAL,
                                short_day_fee REAL,
                                full_day_hours REAL,
                                short_day_hours REAL,
                                government_free_hours REAL,
                                year INTEGER,
                                month INTEGER,
                                weekly_schedule TEXT,
                                monthly_cost REAL)"""
        )
        self.conn.commit()

    def save_to_db(
        self,
        full_day_fee,
        short_day_fee,
        full_day_hours,
        short_day_hours,
        government_free_hours,
        year,
        month,
        weekly_schedule,
        monthly_cost,
    ):
        self.cursor.execute(
            """INSERT INTO childcare_data (full_day_fee, short_day_fee, full_day_hours, short_day_hours, 
                                government_free_hours, year, month, weekly_schedule, monthly_cost) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                full_day_fee,
                short_day_fee,
                full_day_hours,
                short_day_hours,
                government_free_hours,
                year,
                month,
                str(weekly_schedule),
                monthly_cost,
            ),
        )
        self.conn.commit()

    def export_to_excel(self, filename="childcare_data.xlsx"):
        self.cursor.execute("SELECT * FROM childcare_data")
        data = self.cursor.fetchall()
        columns = [description[0] for description in self.cursor.description]

        df = pd.DataFrame(data, columns=columns)
        df.to_excel(filename, index=False)
        print(f"Data exported to {filename}")
