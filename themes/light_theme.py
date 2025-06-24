from .base_theme import BaseTheme

class LightTheme(BaseTheme):
    def apply(self, root):
        root.configure(bg="white")
        for widget in root.winfo_children():
            try:
                widget.configure(bg="white", fg="black")
            except:
                pass