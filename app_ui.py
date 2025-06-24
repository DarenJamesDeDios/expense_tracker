import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from expense import Expense
from expense_manager import ExpenseManager
from themes import ThemeManager

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.manager = ExpenseManager()
        self.sort_order = {'date': False, 'category': False, 'amount': False}
        self.setup_ui()
        self.refresh()
        self.theme = ThemeManager()
        self.theme.apply_light_theme()
        self.current_theme = "light"

    def setup_ui(self):
        self.toggle_theme_button = tk.Button(self.root, text="Toggle Theme", command=self.toggle_theme)
        self.toggle_theme_button.grid(row=0, column=9)

        self.root.title("Expense Tracker")
        self.root.resizable(False, False)

        tk.Label(self.root, text="Date:").grid(row=0, column=0)
        self.date_entry = DateEntry(self.root, date_pattern="yyyy-mm-dd")
        self.date_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Category:").grid(row=0, column=2)
        self.category_combobox = ttk.Combobox(self.root, values=[
            "Food: Groceries", "Food: Dining", "Housing: Rent", "Housing: Utils",
            "Transport: Fuel", "Transport: Public", "Transport: Car Maint",
            "Health: Insurance", "Health: Medical", "Health: Fitness",
            "Entertainment: Movies", "Entertainment: Subs", "Entertainment: Hobbies",
            "Clothing: Apparel", "Education: Tuition", "Education: Supplies",
            "Personal Care: Hair", "Misc: Gifts", "Savings: Retirement", "Savings: Emergency"
        ])
        self.category_combobox.grid(row=0, column=3)

        tk.Label(self.root, text="Amount:").grid(row=0, column=4)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=0, column=5)

        self.add_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=0, column=6)

        self.edit_button = tk.Button(self.root, text="Edit", command=self.edit_expense)
        self.edit_button.grid(row=0, column=7)

        self.delete_button = tk.Button(self.root, text="Delete", command=self.delete_expense)
        self.delete_button.grid(row=0, column=8)

        self.status_label = tk.Label(self.root, text="", fg="red")
        self.status_label.grid(row=1, column=0, columnspan=9)

        columns = ("date", "category", "amount")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)
        for column in columns:
            self.tree.heading(column, text=column.title(), command=lambda col=column: self.sort_by(col))
        self.tree.grid(row=2, column=0, columnspan=9)

        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=2, column=9, sticky='ns')

        self.total_label = tk.Label(self.root, text="Total Expenses: $0.00")
        self.total_label.grid(row=3, column=0, columnspan=9)

        self.summary_text = tk.Text(self.root, height=10, width=30, state=tk.DISABLED)
        self.summary_text.grid(row=4, column=0, columnspan=9)

    def toggle_theme(self):
        if self.current_theme == "light":
            self.theme.apply_dark_theme()
            self.current_theme = "dark"
        else:
            self.theme.apply_light_theme()
            self.current_theme = "light"

    def add_expense(self):
        date = self.date_entry.get()
        category = self.category_combobox.get()
        amount = self.amount_entry.get()
        if date and category and amount:
            try:
                new_expense = Expense(date, category, float(amount))
                self.manager.add_expense(new_expense)
                self.status_label.config(text="Expense added.", fg="green")
                self.refresh()
            except ValueError:
                self.status_label.config(text="Invalid amount format.", fg="red")
        else:
            self.status_label.config(text="Fill all fields.", fg="red")

    def delete_expense(self):
        selected_items = self.tree.selection()
        if selected_items:
            selected_values = self.tree.item(selected_items[0])['values']
            expense_to_delete = Expense(*selected_values)
            self.manager.delete_expense(expense_to_delete)
            self.status_label.config(text="Deleted.", fg="green")
            self.refresh()

    def edit_expense(self):
        selected_items = self.tree.selection()
        if selected_items:
            selected_values = self.tree.item(selected_items[0])['values']
            self.old_expense = Expense(*selected_values)
            self.date_entry.set_date(self.old_expense.date)
            self.category_combobox.set(self.old_expense.category)
            self.amount_entry.delete(0, tk.END)
            self.amount_entry.insert(0, str(self.old_expense.amount))
            self.add_button.config(text="Update", command=self.update_expense)

    def update_expense(self):
        updated_expense = Expense(self.date_entry.get(), self.category_combobox.get(), self.amount_entry.get())
        self.manager.update_expense(self.old_expense, updated_expense)
        self.add_button.config(text="Add Expense", command=self.add_expense)
        self.status_label.config(text="Updated.", fg="green")
        self.refresh()

    def refresh(self):
        self.manager.load_expenses()
        self.tree.delete(*self.tree.get_children())
        for expense in self.manager.expenses:
            self.tree.insert("", tk.END, values=(expense.date, expense.category, f"{expense.amount:.2f}"))
        self.total_label.config(text=f"Total Expenses: ${self.manager.get_total():.2f}")
        self.update_summary()

    def update_summary(self):
        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete(1.0, tk.END)
        for category, summary_data in self.manager.get_summary().items():
            self.summary_text.insert(
                tk.END,
                f"{category}:\n  Total = ${summary_data['total']:.2f}\n  Avg = ${summary_data['average']:.2f}\n\n"
            )
        self.summary_text.config(state=tk.DISABLED)

    def sort_by(self, column_name):
        reverse_sort = not self.sort_order[column_name]
        self.manager.expenses.sort(
            key=lambda expense: getattr(expense, column_name) if column_name != 'amount' else float(expense.amount),
            reverse=reverse_sort
        )
        self.sort_order[column_name] = reverse_sort
        self.refresh()

