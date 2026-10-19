"""
Student Expense Tracker and Budget Management System
Python 3 - uses only standard-library modules.

Data files are created beside this script:
- expenses.json       Persistent expense records
- settings.json       Monthly budget
- expense_report.csv  Generated only when CSV export is selected
"""

import csv
import json
from abc import ABC, abstractmethod
from datetime import date, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "expenses.json"
SETTINGS_FILE = BASE_DIR / "settings.json"
CSV_FILE = BASE_DIR / "expense_report.csv"


class Expense:
    """Represents one expense record."""

    def __init__(self, expense_id, amount, category, description, expense_date):
        self.expense_id = int(expense_id)
        self.amount = float(amount)
        self.category = str(category).strip()
        self.description = str(description).strip()
        self.date = str(expense_date)

    def to_dict(self):
        return {
            "expense_id": self.expense_id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["expense_id"],
            data["amount"],
            data["category"],
            data.get("description", ""),
            data["date"],
        )


class Report(ABC):
    """Abstract base class for reports."""

    @abstractmethod
    def generate(self, expenses):
        """Generate a report from a collection of expenses."""
        raise NotImplementedError


class ConsoleReport(Report):
    """Print category totals and the overall total to the terminal."""

    def generate(self, expenses):
        print("\n========== EXPENSE REPORT ==========")
        if not expenses:
            print("No expenses recorded.")
            return

        totals = {}
        grand_total = 0.0
        for expense in expenses:
            totals[expense.category] = totals.get(expense.category, 0.0) + expense.amount
            grand_total += expense.amount

        for category, amount in sorted(totals.items()):
            print(f"{category}: Rs. {amount:.2f}")
        print("------------------------------------")
        print(f"Total expenses: Rs. {grand_total:.2f}")


class BaseTracker(ABC):
    """Abstract interface for expense tracker implementations."""

    @abstractmethod
    def add_expense(self):
        raise NotImplementedError

    @abstractmethod
    def generate_report(self):
        raise NotImplementedError


class ExpenseTracker(BaseTracker):
    def __init__(self):
        self.__expenses = []
        self.__monthly_budget = 0.0
        self.load_data()

    def get_expenses(self):
        """Return a copy so callers cannot change the internal list directly."""
        return self.__expenses.copy()

    def load_data(self):
        """Load JSON files, starting with empty defaults when files do not exist."""
        try:
            if DATA_FILE.exists():
                with DATA_FILE.open("r", encoding="utf-8") as file:
                    raw_expenses = json.load(file)
                if not isinstance(raw_expenses, list):
                    raise ValueError("expenses.json must contain a JSON list.")
                self.__expenses = [Expense.from_dict(item) for item in raw_expenses]
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            print(f"Warning: Could not load expense data: {error}")
            self.__expenses = []

        try:
            if SETTINGS_FILE.exists():
                with SETTINGS_FILE.open("r", encoding="utf-8") as file:
                    settings = json.load(file)
                self.__monthly_budget = float(settings.get("monthly_budget", 0.0))
                if self.__monthly_budget < 0:
                    raise ValueError("Monthly budget cannot be negative.")
        except (OSError, json.JSONDecodeError, AttributeError, TypeError, ValueError) as error:
            print(f"Warning: Could not load budget settings: {error}")
            self.__monthly_budget = 0.0

    def save_expenses(self):
        """Write all expense records to JSON."""
        temporary_file = DATA_FILE.with_suffix(".json.tmp")
        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(
                [expense.to_dict() for expense in self.__expenses],
                file,
                indent=4,
                ensure_ascii=False,
            )
        temporary_file.replace(DATA_FILE)

    def save_budget(self):
        """Write the monthly budget to JSON."""
        temporary_file = SETTINGS_FILE.with_suffix(".json.tmp")
        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump({"monthly_budget": self.__monthly_budget}, file, indent=4)
        temporary_file.replace(SETTINGS_FILE)

    @staticmethod
    def read_date(prompt):
        value = input(prompt).strip()
        if not value:
            return date.today().isoformat()
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat()

    def add_expense(self):
        try:
            amount = float(input("Enter amount (Rs.): ").strip())
            if amount <= 0:
                print("Amount must be greater than zero.")
                return

            category = input("Enter category: ").strip()
            if not category:
                print("Category cannot be empty.")
                return

            description = input("Enter description (optional): ").strip()
            if not description:
                description = "No description"

            expense_date = self.read_date(
                "Enter date (YYYY-MM-DD), or press Enter for today: "
            )

            next_id = max(
                (expense.expense_id for expense in self.__expenses), default=0
            ) + 1
            new_expense = Expense(
                next_id, amount, category, description, expense_date
            )
            self.__expenses.append(new_expense)

            try:
                self.save_expenses()
            except OSError as error:
                self.__expenses.remove(new_expense)
                print(f"Could not save the expense: {error}")
                return

            print(f"Expense added successfully (ID: {next_id}).")
        except ValueError:
            print("Invalid amount or date. Use a number for the amount and YYYY-MM-DD for the date.")
        except OSError as error:
            print(f"File error: {error}")

    def view_expenses(self):
        if not self.__expenses:
            print("No expenses found.")
            return

        print("\nID | Date | Category | Amount (Rs.) | Description")
        print("-" * 78)
        for expense in sorted(self.__expenses, key=lambda item: (item.date, item.expense_id)):
            print(
                f"{expense.expense_id} | {expense.date} | {expense.category} | "
                f"{expense.amount:.2f} | {expense.description}"
            )

    def search_expenses(self):
        keyword = input("Enter category or description to search: ").strip().lower()
        if not keyword:
            print("Please enter a search term.")
            return

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
                f"ID: {expense.expense_id} | Date: {expense.date} | "
                f"{expense.category} | Rs. {expense.amount:.2f} | "
                f"{expense.description}"
            )

    def delete_expense(self):
        try:
            expense_id = int(input("Enter the expense ID to delete: ").strip())
        except ValueError:
            print("Please enter a valid numeric ID.")
            return

        for index, expense in enumerate(self.__expenses):
            if expense.expense_id == expense_id:
                removed = self.__expenses.pop(index)
                try:
                    self.save_expenses()
                except OSError as error:
                    self.__expenses.insert(index, removed)
                    print(f"Could not save the changes: {error}")
                    return
                print("Expense deleted successfully.")
                return

        print("Expense ID not found.")

    def set_budget(self):
        try:
            budget = float(input("Enter monthly budget (Rs.): ").strip())
            if budget <= 0:
                print("Budget must be greater than zero.")
                return

            old_budget = self.__monthly_budget
            self.__monthly_budget = budget
            try:
                self.save_budget()
            except OSError as error:
                self.__monthly_budget = old_budget
                print(f"Could not save the budget: {error}")
                return
            print("Monthly budget saved.")
        except ValueError:
            print("Please enter a valid numeric budget.")

    def show_budget(self):
        current_month = date.today().strftime("%Y-%m")
        spent = sum(
            expense.amount for expense in self.__expenses
            if expense.date.startswith(current_month)
        )
        remaining = self.__monthly_budget - spent

        print(f"\nMonth: {current_month}")
        print(f"Monthly budget: Rs. {self.__monthly_budget:.2f}")
        print(f"Spent this month: Rs. {spent:.2f}")
        print(f"Remaining budget: Rs. {remaining:.2f}")
        if self.__monthly_budget > 0 and spent > self.__monthly_budget:
            print("Warning: You have exceeded your monthly budget!")

    def generate_report(self):
        ConsoleReport().generate(self.get_expenses())

    def export_csv(self):
        """Export all expense records to a spreadsheet-friendly CSV file."""
        fields = ["expense_id", "date", "category", "amount", "description"]
        try:
            with CSV_FILE.open("w", newline="", encoding="utf-8-sig") as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()
                for expense in sorted(
                    self.__expenses, key=lambda item: (item.date, item.expense_id)
                ):
                    writer.writerow({
                        "expense_id": expense.expense_id,
                        "date": expense.date,
                        "category": expense.category,
                        "amount": f"{expense.amount:.2f}",
                        "description": expense.description,
                    })
            print(f"CSV report exported to: {CSV_FILE.name}")
        except OSError as error:
            print(f"Could not export CSV report: {error}")


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
            tracker.export_csv()
        elif choice == "9":
            print("Thank you for using Student Expense Tracker!")
            break
        else:
            print("Invalid choice. Select a number from 1 to 9.")


if __name__ == "__main__":
    main()
