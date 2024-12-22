import customtkinter as ctk


class ChildCareApp(ctk.CTk):
    def __init__(self, calculator, database):
        super().__init__()
        self.calculator = calculator
        self.database = database

        self.title("Child Care Cost Calculator")
        self.geometry("600x1000")

        # Main scrollable frame
        main_frame = ctk.CTkScrollableFrame(self)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Input fields frame
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(input_frame, text="Full Day Fee (£):").grid(
            row=0, column=0, sticky="e", padx=10, pady=5
        )
        self.full_day_fee_entry = ctk.CTkEntry(input_frame, width=200)
        self.full_day_fee_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(input_frame, text="Short Day Fee (£):").grid(
            row=1, column=0, sticky="e", padx=10, pady=5
        )
        self.short_day_fee_entry = ctk.CTkEntry(input_frame, width=200)
        self.short_day_fee_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(input_frame, text="Full Day Hours (default: 8am-6pm):").grid(
            row=2, column=0, sticky="e", padx=10, pady=5
        )
        self.full_day_hours_entry = ctk.CTkEntry(input_frame, width=200)
        self.full_day_hours_entry.grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkLabel(input_frame, text="Short Day Hours (default: 9am-5pm):").grid(
            row=3, column=0, sticky="e", padx=10, pady=5
        )
        self.short_day_hours_entry = ctk.CTkEntry(input_frame, width=200)
        self.short_day_hours_entry.grid(row=3, column=1, padx=10, pady=5)

        ctk.CTkLabel(input_frame, text="Government Free Hours per Week:").grid(
            row=4, column=0, sticky="e", padx=10, pady=5
        )
        self.government_free_hours_entry = ctk.CTkEntry(input_frame, width=200)
        self.government_free_hours_entry.grid(row=4, column=1, padx=10, pady=5)

        ctk.CTkLabel(input_frame, text="Year (e.g., 2024):").grid(
            row=5, column=0, sticky="e", padx=10, pady=5
        )
        self.year_entry = ctk.CTkEntry(input_frame, width=200)
        self.year_entry.grid(row=5, column=1, padx=10, pady=5)

        ctk.CTkLabel(input_frame, text="Month (1-12):").grid(
            row=6, column=0, sticky="e", padx=10, pady=5
        )
        self.month_entry = ctk.CTkEntry(input_frame, width=200)
        self.month_entry.grid(row=6, column=1, padx=10, pady=5)

        # Schedule frame
        schedule_frame = ctk.CTkFrame(main_frame)
        schedule_frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(schedule_frame, text="Schedule: Select Day Type").grid(
            row=0, column=0, columnspan=4, pady=10
        )

        self.schedule_vars = {}
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for i, day in enumerate(self.days):
            ctk.CTkLabel(schedule_frame, text=day).grid(
                row=i + 1, column=0, sticky="w", padx=10, pady=5
            )

            day_type_var = ctk.StringVar(value="none")
            self.schedule_vars[day] = day_type_var

            ctk.CTkRadioButton(
                schedule_frame, text="Full Day", variable=day_type_var, value="full"
            ).grid(row=i + 1, column=1, padx=10, pady=5)
            ctk.CTkRadioButton(
                schedule_frame, text="Short Day", variable=day_type_var, value="short"
            ).grid(row=i + 1, column=2, padx=10, pady=5)
            ctk.CTkRadioButton(
                schedule_frame, text="None", variable=day_type_var, value="none"
            ).grid(row=i + 1, column=3, padx=10, pady=5)

        # Tax-free childcare option frame
        tax_free_frame = ctk.CTkFrame(main_frame)
        tax_free_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.tax_free_var = ctk.BooleanVar()
        ctk.CTkCheckBox(
            tax_free_frame,
            text="Include Tax-Free Childcare",
            variable=self.tax_free_var,
        ).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(
            tax_free_frame,
            text="For every £8 spent, the government adds £2, up to a maximum of £500 every 3 months (or £2000 per year)",
        ).grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Result display
        result_frame = ctk.CTkFrame(main_frame)
        result_frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(result_frame, text="Monthly Cost (£):").grid(
            row=0, column=0, sticky="e", padx=10, pady=5
        )
        self.result_label = ctk.CTkLabel(result_frame, text="--", font=("Arial", 12))
        self.result_label.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # Buttons frame
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Calculate button
        self.calculate_button = ctk.CTkButton(
            buttons_frame, text="Calculate", command=self.calculate_cost, width=100
        )
        self.calculate_button.grid(row=0, column=0, padx=10, pady=10)

        # Export button
        self.export_button = ctk.CTkButton(
            buttons_frame,
            text="Export to Excel",
            command=self.export_to_excel,
            width=100,
        )
        self.export_button.grid(row=0, column=1, padx=10, pady=10)

        # Clear button
        self.clear_button = ctk.CTkButton(
            buttons_frame, text="Clear", command=self.clear_fields, width=100
        )
        self.clear_button.grid(row=0, column=2, padx=10, pady=10)

        # Bind resizing event to adjust fonts
        self.bind("<Configure>", self.adjust_font_size)

    def calculate_cost(self):
        try:
            full_day_fee = float(self.full_day_fee_entry.get())
            short_day_fee = (
                float(self.short_day_fee_entry.get())
                if self.short_day_fee_entry.get()
                else 0
            )

            full_day_hours = self.calculator.parse_time_range(
                self.full_day_hours_entry.get(),
                default_full="8am-6pm",
                is_full_day=True,
            )
            short_day_hours = self.calculator.parse_time_range(
                self.short_day_hours_entry.get(),
                default_short="9am-5pm",
                is_full_day=False,
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
            self.result_label.configure(text=f"£{monthly_cost:.2f}")

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
            self.result_label.configure(text="Error")
            print(f"Invalid input: {e}")

    def export_to_excel(self):
        try:
            self.database.export_to_excel()
            print("Data exported to childcare_data.xlsx")
        except Exception as e:
            print(f"Failed to export data: {e}")

    def adjust_font_size(self, event):
        new_size = max(14, int(event.width / 50))
        self.result_label.configure(font=("Arial", new_size))

    def clear_fields(self):
        self.full_day_fee_entry.delete(0, ctk.END)
        self.short_day_fee_entry.delete(0, ctk.END)
        self.full_day_hours_entry.delete(0, ctk.END)
        self.short_day_hours_entry.delete(0, ctk.END)
        self.government_free_hours_entry.delete(0, ctk.END)
        self.year_entry.delete(0, ctk.END)
        self.month_entry.delete(0, ctk.END)
        for day in self.days:
            self.schedule_vars[day].set("none")
        self.tax_free_var.set(False)
        self.result_label.configure(text="--")


if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")  # Modes: "System" (default), "Dark", "Light"
    ctk.set_default_color_theme(
        "blue"
    )  # Themes: "blue" (default), "green", "dark-blue"

    calculator = ChildCareCalculator()
    database = DatabaseHandler()
    app = ChildCareApp(calculator, database)
    app.mainloop()
