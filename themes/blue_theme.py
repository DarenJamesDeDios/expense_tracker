from base_theme import BaseTheme

class BlueTheme(BaseTheme):
    def apply(self, root):
        root.configure(bg="#e0f7fa")
        for widget in root.winfo_children():
            try:
                widget.configure(bg="#e0f7fa", fg="#01579b")
            except:
                pass