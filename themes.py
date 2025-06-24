#Planning to add light and dark theme for the user to choose their preferred theme.
from tkinter import ttk

class ThemeManager:
    def __init__(self):
        self.style = ttk.Style()

    def apply_light_theme(self):
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#fff", foreground="#000", fieldbackground="#fff")
        self.style.map("Treeview", background=[("selected", "#007acc")], foreground=[("selected", "white")])
        self.style.configure("TButton", background="#007acc", foreground="white", padding=5)
        self.style.configure("TLabel", font=("Segoe UI", 10))
