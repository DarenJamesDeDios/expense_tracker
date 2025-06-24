from base_theme import BaseTheme

class DarkTheme(BaseTheme):
    def apply(self, root):
        root.configure(bg="black")
        for widget in root.winfo_children():
            try:
                widget.configure(bg="black", fg="white")
            except:
                pass