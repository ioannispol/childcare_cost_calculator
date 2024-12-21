import tkinter as tk
from calendar import monthrange
from datetime import datetime
import sqlite3
import pandas as pd


class ChildCareCalculator:
    def __init__(
        self,
        full_day_fee,
        short_day_fee,
        full_day_hours,
        short_day_hours,
        government_free_hours_per_week,
        weekly_schedule,
    ):
        self.full_day_fee = full_day_fee
        self.short_day_fee = short_day_fee
        self.full_day_hours = full_day_hours
        self.short_day_hours = short_day_hours
        self.government_free_hours_per_week = government_free_hours_per_week
        self.weekly_schedule = weekly_schedule

    def calculate_monthly_cost(self, year, month):
        days_in_month = monthrange(year, month)[1]
        total_monthly_cost = 0
        total_monthly_hours = 0

        for day in range(1, days_in_month + 1):
            weekday = (day - 1) % 7  # Monday=0, Tuesday=1, ..., Sunday=6
            if weekday in self.weekly_schedule:
                if self.weekly_schedule[weekday] == "full":
                    total_monthly_cost += self.full_day_fee
                    total_monthly_hours += self.full_day_hours
                elif self.weekly_schedule[weekday] == "short":
                    total_monthly_cost += self.short_day_fee
                    total_monthly_hours += self.short_day_hours

        # Deduct government free hours for the month
        free_hours_per_month = (
            self.government_free_hours_per_week * 4.33
        )  # Approximate weeks in a month
        paid_hours = max(total_monthly_hours - free_hours_per_month, 0)

        # Calculate the final adjusted cost
        hourly_rate_full = self.full_day_fee / self.full_day_hours
        hourly_rate_short = self.short_day_fee / self.short_day_hours
        adjusted_cost = paid_hours * (
            hourly_rate_full if total_monthly_hours > 0 else hourly_rate_short
        )

        return adjusted_cost


# Helper function to parse time ranges
def parse_time_range(time_range, default):
    if not time_range:
        return default
    try:
        start_time, end_time = time_range.split("-")
        start_time = datetime.strptime(start_time.strip(), "%I%p")
        end_time = datetime.strptime(end_time.strip(), "%I%p")
        duration = (end_time - start_time).seconds / 3600
        return duration
    except Exception as e:
        raise ValueError(
            f"Invalid time range format: {time_range}. Expected format: '8am-6pm'. {e}"
        )


class ChildCareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Child Care Cost Calculator")

        # Initialize database
        self.init_db()

        # Input fields
        tk.Label(root, text="Full Day Fee (£):").grid(row=0, column=0, sticky="e")
        self.full_day_fee_entry = tk.Entry(root)
        self.full_day_fee_entry.grid(row=0, column=1)

        tk.Label(root, text="Short Day Fee (£):").grid(row=1, column=0, sticky="e")
        self.short_day_fee_entry = tk.Entry(root)
        self.short_day_fee_entry.grid(row=1, column=1)

        tk.Label(root, text="Full Day Hours (e.g., 8am-6pm):").grid(
            row=2, column=0, sticky="e"
        )
        self.full_day_hours_entry = tk.Entry(root)
        self.full_day_hours_entry.grid(row=2, column=1)

        tk.Label(root, text="Short Day Hours (e.g., 9am-5pm):").grid(
            row=3, column=0, sticky="e"
        )
        self.short_day_hours_entry = tk.Entry(root)
        self.short_day_hours_entry.grid(row=3, column=1)

        tk.Label(root, text="Government Free Hours per Week:").grid(
            row=4, column=0, sticky="e"
        )
        self.government_free_hours_entry = tk.Entry(root)
        self.government_free_hours_entry.grid(row=4, column=1)

        tk.Label(root, text="Year (e.g., 2024):").grid(row=5, column=0, sticky="e")
        self.year_entry = tk.Entry(root)
        self.year_entry.grid(row=5, column=1)

        tk.Label(root, text="Month (1-12):").grid(row=6, column=0, sticky="e")
        self.month_entry = tk.Entry(root)
        self.month_entry.grid(row=6, column=1)

        tk.Label(root, text="Schedule: Select Day Type").grid(
            row=7, column=0, sticky="ne"
        )

        # Schedule selection
        self.schedule_vars = {}
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.schedule_frame = tk.Frame(root)
        self.schedule_frame.grid(row=7, column=1, sticky="w")
        for i, day in enumerate(self.days):
            frame = tk.Frame(self.schedule_frame)
            frame.grid(row=i, column=0, sticky="w")
            tk.Label(frame, text=day).grid(row=0, column=0, sticky="w")

            day_type_var = tk.StringVar(value="none")
            self.schedule_vars[day] = day_type_var

            tk.Radiobutton(
                frame, text="Full Day", variable=day_type_var, value="full"
            ).grid(row=0, column=1, sticky="w")
            tk.Radiobutton(
                frame, text="Short Day", variable=day_type_var, value="short"
            ).grid(row=0, column=2, sticky="w")
            tk.Radiobutton(
                frame, text="None", variable=day_type_var, value="none"
            ).grid(row=0, column=3, sticky="w")

        # Result display
        tk.Label(root, text="Monthly Cost (£):").grid(row=8, column=0, sticky="e")
        self.result_label = tk.Label(root, text="--", font=("Arial", 12))
        self.result_label.grid(row=8, column=1, sticky="w")

        # Calculate button
        self.calculate_button = tk.Button(
            root, text="Calculate", command=self.calculate_cost
        )
        self.calculate_button.grid(row=9, column=0, columnspan=2)

        # Export button
        self.export_button = tk.Button(
            root, text="Export to Excel", command=self.export_to_excel
        )
        self.export_button.grid(row=10, column=0, columnspan=2)

        # Bind resizing event to adjust fonts
        self.root.bind("<Configure>", self.adjust_font_size)

    def init_db(self):
        self.conn = sqlite3.connect("childcare.db")
        self.cursor = self.conn.cursor()
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

    def calculate_cost(self):
        try:
            full_day_fee = float(self.full_day_fee_entry.get())
            short_day_fee = float(self.short_day_fee_entry.get())

            full_day_hours = parse_time_range(
                self.full_day_hours_entry.get(), 10
            )  # Default 8am-6pm = 10 hours
            short_day_hours = parse_time_range(
                self.short_day_hours_entry.get(), 8
            )  # Default 9am-5pm = 8 hours

            government_free_hours_per_week = float(
                self.government_free_hours_entry.get()
            )

            year = int(self.year_entry.get())
            month = int(self.month_entry.get())

            weekly_schedule = {}
            for i, day in enumerate(self.days):
                day_type = self.schedule_vars[day].get()
                if day_type != "none":
                    weekly_schedule[i] = day_type

            calculator = ChildCareCalculator(
                full_day_fee=full_day_fee,
                short_day_fee=short_day_fee,
                full_day_hours=full_day_hours,
                short_day_hours=short_day_hours,
                government_free_hours_per_week=government_free_hours_per_week,
                weekly_schedule=weekly_schedule,
            )

            monthly_cost = calculator.calculate_monthly_cost(year, month)
            self.result_label.config(text=f"£{monthly_cost:.2f}")

            # Save data to the database
            self.save_to_db(
                full_day_fee,
                short_day_fee,
                full_day_hours,
                short_day_hours,
                government_free_hours_per_week,
                year,
                month,
                weekly_schedule,
                monthly_cost,
            )

        except Exception as e:
            self.result_label.config(text="Error")
            print(f"Invalid input: {e}")

    def export_to_excel(self):
        try:
            self.cursor.execute("SELECT * FROM childcare_data")
            data = self.cursor.fetchall()
            columns = [description[0] for description in self.cursor.description]

            df = pd.DataFrame(data, columns=columns)
            df.to_excel("childcare_data.xlsx", index=False)
            print("Data exported to childcare_data.xlsx")
        except Exception as e:
            print(f"Failed to export data: {e}")

    def adjust_font_size(self, event):
        new_size = max(
            12, int(event.width / 50)
        )  # Adjust font size dynamically based on window width
        self.result_label.config(font=("Arial", new_size))


if __name__ == "__main__":
    root = tk.Tk()
    app = ChildCareApp(root)
    root.mainloop()
