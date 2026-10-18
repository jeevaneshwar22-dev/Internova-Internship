
import json
import csv
import os
from datetime import datetime
from abc import ABC, abstractmethod

DATA_FILE = "expenses.json"
SETTINGS_FILE = "settings.json"


# ---------- Expense Class ----------
class Expense:
    def __init__(self, expense_id, amount, category, description, date):
        self.expense_id = expense_id
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date

    def to_dict(self):
        return {
            "expense_id": self.expense_id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["expense_id"],
            float(data["amount"]),
            data["category"],
            data["description"],
            data["date"]
        )


# ---------- Abstraction and Polymorphism ----------
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

        totals = {}
        grand_total = 0

        for expense in expenses:
            totals[expense.category] = (
                totals.get(expense.category, 0) + expense.amount
            )
            grand_total += expense.amount

        for category, amount in sorted(totals.items()):
            print(f"{category}: Rs. {amount:.2f}")

        print("------------------------------------")
        print(f"Total expenses: Rs. {grand_total:.2f}")


class CSVReport(Report):
    def generate(self, expenses):
        filename = "expense_report.csv"

        with open(filename, "w", newline="", encoding="utf-8") as file:
            fields = [
                "expense_id", "amount", "category",
                "description", "date"
            ]
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()

            for expense in expenses:
                writer.writerow(expense.to_dict())

        print(f"Report exported to {filename}")


# ---------- Base Class: Inheritance ----------
class BaseTracker(ABC):
    @abstractmethod
    def add_expense(self):
        pass

    @abstractmethod
    def generate_report(self):
        pass


# ---------- Main Expense Tracker ----------
class ExpenseTracker(BaseTracker):
    def __init__(self):
        self.__expenses = []  # Encapsulation
        self.__monthly_budget = 0.0
        self.load_data()

    def load_data(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r", encoding="utf-8") as file:
                    records = json.load(file)

                self.__expenses = [
                    Expense.from_dict(record) for record in records
                ]

            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
                    settings = json.load(file)

                self.__monthly_budget = float(
                    settings.get("monthly_budget", 0)
                )

        except (OSError, json.JSONDecodeError, ValueError,
                KeyError, TypeError) as error:
            print("Warning: Could not load saved data:", error)
            self.__expenses = []
            self.__monthly_budget = 0.0

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(
                [expense.to_dict() for expense in self.__expenses],
                file,
                indent=4
            )

        with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
            json.dump(
                {"monthly_budget": self.__monthly_budget},
                file,
                indent=4
            )

    def get_expenses(self):
        # Return a copy instead of exposing the private list.
        return self.__expenses.copy()

    def add_expense(self):
        try:
            amount = float(input("Enter amount (Rs.): "))

            if not (0 < amount < float("inf")):
                print("Amount must be a positive, finite number.")
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

            expense_id = max(
                (expense.expense_id for expense in self.__expenses),
                default=0
            ) + 1

            expense = Expense(
                expense_id, amount, category, description, date
            )
            self.__expenses.append(expense)
            self.save_data()

            print("Expense added successfully!")

        except ValueError:
            print("Invalid amount or date. Please try again.")
        except OSError as error:
            print("Could not save expense:", error)

    def view_expenses(self):
        expenses = self.get_expenses()

        if not expenses:
            print("No expenses found.")
            return

        print("\nID | Date | Category | Amount | Description")
        print("-" * 65)

        for expense in expenses:
            print(
                f"{expense.expense_id} | {expense.date} | "
                f"{expense.category} | Rs. {expense.amount:.2f} | "
                f"{expense.description}"
            )

    def search_expenses(self):
        keyword = input("Enter category or description to search: ")
        keyword = keyword.strip().lower()

        results = [
            expense for expense in self.__expenses
            if keyword in expense.category.lower()
            or keyword in expense.description.lower()
        ]

        if not results:
            print("No matching expenses found.")
        else:
            for expense in results:
                print(expense.to_dict())

    def delete_expense(self):
        try:
            expense_id = int(input("Enter expense ID to delete: "))

            for expense in self.__expenses:
                if expense.expense_id == expense_id:
                    self.__expenses.remove(expense)
                    self.save_data()
                    print("Expense deleted successfully.")
                    return

            print("Expense ID not found.")

        except ValueError:
            print("Please enter a valid numeric ID.")
        except OSError as error:
            print("Could not save changes:", error)

    def set_budget(self):
        try:
            budget = float(input("Enter monthly budget (Rs.): "))

            if not (0 < budget < float("inf")):
                print("Budget must be a positive, finite number.")
                return

            self.__monthly_budget = budget
            self.save_data()
            print("Monthly budget saved.")

        except ValueError:
            print("Please enter a valid budget.")
        except OSError as error:
            print("Could not save budget:", error)

    def show_budget(self):
        current_month = datetime.now().strftime("%Y-%m")

        total = sum(
            expense.amount for expense in self.__expenses
            if expense.date.startswith(current_month)
        )

        print(f"\nMonthly budget: Rs. {self.__monthly_budget:.2f}")
        print(f"Spent this month: Rs. {total:.2f}")

        remaining = self.__monthly_budget - total
        print(f"Remaining budget: Rs. {remaining:.2f}")

        if self.__monthly_budget > 0 and total > self.__monthly_budget:
            print("Warning: You have exceeded your monthly budget!")

    def generate_report(self):
        report = ConsoleReport()
        report.generate(self.get_expenses())

    def export_report(self):
        # Polymorphism: CSVReport uses the same generate() interface.
        report = CSVReport()
        report.generate(self.get_expenses())


# ---------- Main Menu ----------
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
        print("8. Export Report to CSV")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ").strip()

        try:
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
                tracker.export_report()
            elif choice == "9":
                print("Thank you for using Student Expense Tracker!")
                break
            else:
                print("Invalid choice. Select a number from 1 to 9.")

        except OSError as error:
            print("File operation failed:", error)


if __name__ == "__main__":
    main()
