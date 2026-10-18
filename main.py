from datetime import datetime
import os
from abc import ABC, abstractmethod

DATA_FILE = "expenses.txt"
SETTINGS_FILE = "settings.txt"


# Represents one expense
class Expense:
    def __init__(self, expense_id, amount, category, description, date):
        self.expense_id = expense_id
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date

    def to_line(self):
        # Replace the separator if it appears in user-entered text.
        category = self.category.replace("|", "/")
        description = self.description.replace("|", "/")
        return (
            f"{self.expense_id}|{self.amount}|{category}|"
            f"{description}|{self.date}\n"
        )


# Abstraction: every report class must implement generate()
class Report(ABC):
    @abstractmethod
    def generate(self, expenses):
        pass


class ConsoleReport(Report):
    def generate(self, expenses):
        print("\n========== EXPENSE REPORT ==========")

        if not expenses:
            print("No expenses recorded.")
            return

        category_totals = {}
        grand_total = 0.0

        for expense in expenses:
            category_totals[expense.category] = (
                category_totals.get(expense.category, 0.0) + expense.amount
            )
            grand_total += expense.amount

        for category, amount in sorted(category_totals.items()):
            print(f"{category}: Rs. {amount:.2f}")

        print("------------------------------------")
        print(f"Total expenses: Rs. {grand_total:.2f}")


# Base class for the tracker
class BaseTracker(ABC):
    @abstractmethod
    def add_expense(self):
        pass

    @abstractmethod
    def generate_report(self):
        pass


class ExpenseTracker(BaseTracker):
    def __init__(self):
        self.__expenses = []  # Encapsulation
        self.__monthly_budget = 0.0
        self.load_data()

    def get_expenses(self):
        # Return a copy so callers cannot directly change the private list.
        return self.__expenses.copy()

    def load_data(self):
        """Load expense records from a plain text file."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as file:
                    for line in file:
                        parts = line.rstrip("\n").split("|")
                        if len(parts) != 5:
                            continue

                        expense_id, amount, category, description, date = parts
                        self.__expenses.append(
                            Expense(
                                int(expense_id),
                                float(amount),
                                category,
                                description,
                                date
                            )
                        )
            except (OSError, ValueError) as error:
                print("Warning: Could not load expense data:", error)
                self.__expenses = []

        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
                    value = file.readline().strip()
                    if value:
                        self.__monthly_budget = float(value)
            except (OSError, ValueError) as error:
                print("Warning: Could not load budget settings:", error)
                self.__monthly_budget = 0.0

    def save_expenses(self):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            for expense in self.__expenses:
                file.write(expense.to_line())

    def save_budget(self):
        with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
            file.write(str(self.__monthly_budget) + "\n")

    def add_expense(self):
        try:
            amount = float(input("Enter amount (Rs.): "))
            if amount <= 0:
                print("Amount must be greater than zero.")
                return

            category = input("Enter category: ").strip()
            description = input("Enter description: ").strip()
            date = input(
                "Enter date (YYYY-MM-DD), or press Enter for today: "
            ).strip()

            if not category:
                print("Category cannot be empty.")
                return

            if not description:
                description = "No description"

            if not date:
                date = datetime.now().strftime("%Y-%m-%d")
            else:
                datetime.strptime(date, "%Y-%m-%d")

            next_id = max(
                (expense.expense_id for expense in self.__expenses),
                default=0
            ) + 1

            self.__expenses.append(
                Expense(next_id, amount, category, description, date)
            )
            self.save_expenses()
            print("Expense added successfully.")

        except ValueError:
            print("Invalid amount or date. Please try again.")
        except OSError as error:
            print("Could not save the expense:", error)

    def view_expenses(self):
        if not self.__expenses:
            print("No expenses found.")
            return

        print("\nID | Date | Category | Amount | Description")
        print("-" * 70)
        for expense in self.__expenses:
            print(
                f"{expense.expense_id} | {expense.date} | "
                f"{expense.category} | Rs. {expense.amount:.2f} | "
                f"{expense.description}"
            )

    def search_expenses(self):
        keyword = input("Enter category or description to search: ")
        keyword = keyword.strip().lower()

        matches = [
            expense for expense in self.__expenses
            if keyword in expense.category.lower()
            or keyword in expense.description.lower()
        ]

        if not matches:
            print("No matching expenses found.")
            return

        for expense in matches:
            print(
                f"ID: {expense.expense_id}, Date: {expense.date}, "
                f"Category: {expense.category}, Amount: Rs. "
                f"{expense.amount:.2f}, Description: {expense.description}"
            )

    def delete_expense(self):
        try:
            expense_id = int(input("Enter the expense ID to delete: "))

            for expense in self.__expenses:
                if expense.expense_id == expense_id:
                    self.__expenses.remove(expense)
                    self.save_expenses()
                    print("Expense deleted successfully.")
                    return

            print("Expense ID not found.")

        except ValueError:
            print("Please enter a valid numeric ID.")
        except OSError as error:
            print("Could not save the changes:", error)

    def set_budget(self):
        try:
            budget = float(input("Enter monthly budget (Rs.): "))
            if budget <= 0:
                print("Budget must be greater than zero.")
                return

            self.__monthly_budget = budget
            self.save_budget()
            print("Monthly budget saved.")

        except ValueError:
            print("Please enter a valid budget.")
        except OSError as error:
            print("Could not save the budget:", error)

    def show_budget(self):
        current_month = datetime.now().strftime("%Y-%m")
        spent = sum(
            expense.amount for expense in self.__expenses
            if expense.date.startswith(current_month)
        )

        print(f"\nMonthly budget: Rs. {self.__monthly_budget:.2f}")
        print(f"Spent this month: Rs. {spent:.2f}")
        print(f"Remaining budget: Rs. {self.__monthly_budget - spent:.2f}")

        if self.__monthly_budget > 0 and spent > self.__monthly_budget:
            print("Warning: You have exceeded your monthly budget!")

    def generate_report(self):
        report = ConsoleReport()
        report.generate(self.get_expenses())


def main():
    tracker = ExpenseTracker()

    while True:
        print("\n===== STUDENT EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Search Expenses")
        print("4. Delete Expense")
        print("5. Set Monthly Budget")
        print("6. View Monthly Budget")
        print("7. Generate Expense Report")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            tracker.add_expense()
        elif choice == "2":
            tracker.view_expenses()
        elif choice == "3":
            tracker.search_expenses()
        elif choice == "4":
            tracker.delete_expense()
        elif choice == "5":
            tracker.set_budget()
        elif choice == "6":
            tracker.show_budget()
        elif choice == "7":
            tracker.generate_report()
        elif choice == "8":
            print("Thank you for using Student Expense Tracker!")
            break
        else:
            print("Invalid choice. Select a number from 1 to 8.")


if __name__ == "__main__":
    main()
