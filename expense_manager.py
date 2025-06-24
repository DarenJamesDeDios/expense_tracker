import csv
import os
from collections import defaultdict
from expense import Expense

class ExpenseManager:
    def __init__(self, filename="finances.csv"):
        self.filename = filename
        self.expenses = []
        self.category_totals = defaultdict(float)
        self.category_counts = defaultdict(int)

    def load_expenses(self):
        self.expenses.clear()
        self.category_totals.clear()
        self.category_counts.clear()
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 3:
                        expense = Expense(*row)
                        self.expenses.append(expense)
                        self.category_totals[expense.category] += expense.amount
                        self.category_counts[expense.category] += 1

    def save_expenses(self):
        with open(self.filename, "w", newline="") as file:
            writer = csv.writer(file)
            for expense in self.expenses:
                writer.writerow([expense.date, expense.category, f"{expense.amount:.2f}"])

    def add_expense(self, expense):
        self.expenses.append(expense)
        self.category_totals[expense.category] += expense.amount
        self.category_counts[expense.category] += 1
        self.save_expenses()

    def delete_expense(self, target_expense):
        self.expenses = [
            expense for expense in self.expenses
            if not (
                expense.date == target_expense.date and
                expense.category == target_expense.category and
                expense.amount == target_expense.amount
            )
        ]
        self.save_expenses()
        self.load_expenses()

    def update_expense(self, old_expense, new_expense):
        self.delete_expense(old_expense)
        self.add_expense(new_expense)

    def get_total(self):
        return sum(expense.amount for expense in self.expenses)

    def get_summary(self):
        return {
            category: {
                'total': total_amount,
                'average': total_amount / self.category_counts[category] if self.category_counts[category] > 0 else 0
            }
            for category, total_amount in self.category_totals.items()
        }