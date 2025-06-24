from base_theme import BaseTheme

class OrangeTheme(BaseTheme):
    def apply(self, root):
        root.configure(bg="#fff3e0")  # light orange
        for widget in root.winfo_children():
            try:
                widget.configure(bg="#fff3e0", fg="#e65100")  # deep orange
            except:
                pass