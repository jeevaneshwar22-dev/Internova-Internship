# Student Expense Tracker

## 1. Project Title
**Student Expense Tracker and Budget Management System**

## 2. Project Description
The Student Expense Tracker is a Python-based application designed to help students manage their daily expenses and monthly budgets. It allows users to add, view, search, and delete expense records, monitor monthly spending, and generate expense reports.

The application uses JSON files to store expense records and budget settings, ensuring that data remains available even after the program is closed. It is developed as a practical project to demonstrate Python programming concepts learned during the internship.

## 3. Features
- Add daily expenses with amount, category, description, and date.
- View all recorded expenses.
- Search expenses by category or description.
- Delete expense records using their IDs.
- Set and track a monthly budget.
- Calculate monthly spending and remaining budget.
- Generate category-wise expense reports.
- Export expense reports to CSV format.
- Store data persistently using JSON files.
- Handle invalid inputs and file-related errors.
- Provide an interactive, menu-driven interface.

## 4. Technologies Used
- **Programming Language:** Python 3
- **Data Storage:** JSON
- **Report Export:** CSV
- **Python Libraries:** `json`, `csv`, `os`, `datetime`, `abc`
- **Development Environment:** Visual Studio Code or Python IDLE
- **Version Control:** Git
- **Code Hosting:** GitHub

## 5. Python Concepts Used
This project demonstrates the following concepts covered during Weeks 1–6 of the internship:

- **Python Fundamentals:** Variables, data types, input, and output.
- **Operators and Type Casting:** Arithmetic operations and conversion of user input.
- **Conditional Statements:** Input validation and menu selection.
- **Loops:** Repeated execution of the menu and iteration through expense records.
- **Functions:** Modular implementation of application features.
- **Data Structures:** Lists and dictionaries for storing and processing data.
- **File Handling:** Reading and writing JSON and CSV files.
- **Exception Handling:** Handling invalid inputs and file errors using `try` and `except`.
- **Python Libraries:** Using built-in modules for dates, files, JSON, CSV, and abstract classes.
- **Classes and Objects:** Implementing `Expense`, `ExpenseTracker`, and report classes.
- **Constructors:** Initializing objects using `__init__()`.
- **Inheritance:** Extending abstract base classes.
- **Polymorphism:** Using different report classes with a common `generate()` method.
- **Encapsulation:** Protecting internal expense data using private attributes.
- **Abstraction:** Defining abstract classes and methods.
- **Git and GitHub:** Tracking code changes and hosting the project repository.

## 6. Installation/Setup

### Prerequisites
- Python 3 installed on your computer.
- Visual Studio Code, Python IDLE, or another Python editor.
- Git installed (optional, for version control).

### Steps
1. Download and install Python from https://www.python.org/downloads/.
2. Create a folder named `StudentExpenseTracker`.
3. Save the project source code as `main.py` inside that folder.
4. Open the folder in Visual Studio Code or a terminal.
5. Verify Python installation by running:

   ```bash
   python --version
   ```

6. No external packages are required because the project uses Python's built-in libraries.

## 7. How to Run the Project

1. Open a terminal in the project folder.
2. Run the following command:

   ```bash
   python main.py
   ```

   On Windows, you can also use:

   ```bash
   py main.py
   ```

3. The main menu will appear in the terminal.
4. Select an option from 1 to 9 to perform an operation:
   - Add Expense
   - View All Expenses
   - Search Expenses
   - Delete Expense
   - Set Monthly Budget
   - View Monthly Budget
   - Generate Expense Report
   - Export Report to CSV
   - Exit

5. Follow the prompts to enter expense details or perform the selected operation.

The application automatically creates `expenses.json` and `settings.json` when data is saved. The file `expense_report.csv` is generated when the CSV export option is selected.

## 8. Future Improvements
- Develop a graphical user interface using Tkinter.
- Create a web-based version using Flask or Django.
- Add user registration and login functionality.
- Introduce expense charts and visual analytics.
- Add monthly and yearly spending comparisons.
- Support editing existing expense records.
- Implement category-wise spending limits and budget alerts.
- Add database integration using SQLite or MySQL.
- Generate downloadable PDF reports.
- Add automated unit tests to improve reliability.

---

**Project Type:** Python Final Internship Project  
**Domain:** Personal Finance and Expense Management  
**Developed Using:** Python 3

**Conclusion:** The Student Expense Tracker provides a simple and practical way to record expenses, manage budgets, and generate reports while demonstrating the core Python concepts covered during the internship.