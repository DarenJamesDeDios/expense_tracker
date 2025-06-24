from base_theme import BaseTheme

class PastelTheme(BaseTheme):
    def apply(self, root):
        root.configure(bg="#fce4ec")  # pastel pink
        for widget in root.winfo_children():
            try:
                widget.configure(bg="#fce4ec", fg="#6a1b9a")  # purple text
            except:
                pass