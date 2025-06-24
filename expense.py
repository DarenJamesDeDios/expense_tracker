# Create a class program that can record the date, category, and amount 
class Expense:
    def __init__(self, date, category, amount):
        self.date = date
        self.category = category
        self.amount = float(amount)