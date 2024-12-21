import tkinter as tk

class ChildCareApp:
    def __init__(self, root, calculator, database):
        self.root = root
        self.calculator = calculator
        self.database = database

        self.root.title("Child Care Cost Calculator")

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

        # Tax-free childcare option
        self.tax_free_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Include Tax-Free Childcare", variable=self.tax_free_var).grid(row=8, column=0, columnspan=2)
        tk.Label(root, text="For every £8 spent, the government adds £2, up to a maximum of £500 every 3 months (or £2000 per year)").grid(row=9, column=0, columnspan=2)

        # Result display
        tk.Label(root, text="Monthly Cost (£):").grid(row=10, column=0, sticky="e")
        self.result_label = tk.Label(root, text="--", font=("Arial", 12))
        self.result_label.grid(row=10, column=1, sticky="w")

        # Calculate button
        self.calculate_button = tk.Button(
            root, text="Calculate", command=self.calculate_cost
        )
        self.calculate_button.grid(row=11, column=0, columnspan=2)

        # Export button
        self.export_button = tk.Button(
            root, text="Export to Excel", command=self.export_to_excel
        )
        self.export_button.grid(row=12, column=0, columnspan=2)

        # Bind resizing event to adjust fonts
        self.root.bind("<Configure>", self.adjust_font_size)

    def calculate_cost(self):
        try:
            full_day_fee = float(self.full_day_fee_entry.get())
            short_day_fee = float(self.short_day_fee_entry.get())

            full_day_hours = self.calculator.parse_time_range(
                self.full_day_hours_entry.get(), 10
            )
            short_day_hours = self.calculator.parse_time_range(
                self.short_day_hours_entry.get(), 8
            )

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

            include_tax_free = self.tax_free_var.get()

            monthly_cost = self.calculator.calculate_monthly_cost(
                full_day_fee,
                short_day_fee,
                full_day_hours,
                short_day_hours,
                government_free_hours_per_week,
                weekly_schedule,
                year,
                month,
                include_tax_free,
            )
            self.result_label.config(text=f"£{monthly_cost:.2f}")

            self.database.save_to_db(
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
            self.database.export_to_excel()
            print("Data exported to childcare_data.xlsx")
        except Exception as e:
            print(f"Failed to export data: {e}")

    def adjust_font_size(self, event):
        new_size = max(14, int(event.width / 50))
        self.result_label.config(font=("Arial", new_size))