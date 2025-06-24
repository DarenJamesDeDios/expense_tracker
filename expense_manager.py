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
            for e in self.expenses:
                writer.writerow([e.date, e.category, f"{e.amount:.2f}"])

    def add_expense(self, expense):
        self.expenses.append(expense)
        self.category_totals[expense.category] += expense.amount
        self.category_counts[expense.category] += 1
        self.save_expenses()

    def delete_expense(self, target):
        self.expenses = [e for e in self.expenses if not (
            e.date == target.date and e.category == target.category and e.amount == target.amount)]
        self.save_expenses()
        self.load_expenses()

    def update_expense(self, old, new):
        self.delete_expense(old)
        self.add_expense(new)

    def get_total(self):
        return sum(e.amount for e in self.expenses)

    def get_summary(self):
        return {
            cat: {
                'total': total,
                'average': total / self.category_counts[cat] if self.category_counts[cat] > 0 else 0
            }
            for cat, total in self.category_totals.items()
        }
    