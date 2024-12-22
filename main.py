import customtkinter as ctk

from ui import ChildCareApp
from childcare_calculator import ChildCareCalculator
from database_handler import DatabaseHandler

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")  # Modes: "System" (default), "Dark", "Light"
    ctk.set_default_color_theme(
        "blue"
    )  # Themes: "blue" (default), "green", "dark-blue"

    calculator = ChildCareCalculator()
    database = DatabaseHandler()
    app = ChildCareApp(calculator, database)
    app.mainloop()
