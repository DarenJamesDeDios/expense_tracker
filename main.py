import tkinter as tk
from app_ui import ExpenseApp

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()
