from tkinter import Tk
from ui import ChildCareApp
from childcare_calculator import ChildCareCalculator
from database_handler import DatabaseHandler

if __name__ == "__main__":
    root = Tk()

    database = DatabaseHandler()
    calculator = ChildCareCalculator()

    app = ChildCareApp(root, calculator, database)

    root.mainloop()
