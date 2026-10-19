# Student Expense Tracker and Budget Management System

A Python-based, menu-driven application that helps students record daily expenses, manage a monthly budget, analyze spending, and export expense records to CSV.

## 1. Project Overview

Managing daily expenses can be difficult for students who want to track their spending and stay within a monthly budget. The Student Expense Tracker and Budget Management System provides a simple way to record expenses, review spending patterns, and monitor budget usage.

The application is developed using Python and demonstrates fundamental programming concepts, file handling, exception handling, and object-oriented programming.

## 2. Features

- **Add Expense:** Record an expense with its amount, category, description, and date.
- **View All Expenses:** Display saved expense records.
- **Search Expenses:** Find expenses using category or description keywords.
- **Delete Expense:** Remove a record using its unique expense ID.
- **Set Monthly Budget:** Configure a monthly spending limit.
- **View Monthly Budget:** Review the monthly budget, amount spent, and remaining balance.
- **Generate Expense Report:** Display category-wise expense totals and overall expenditure.
- **Export Report to CSV:** Export expense records to a CSV file that can be opened in spreadsheet applications.
- **Persistent Storage:** Store expense records and budget settings in JSON files.
- **Input Validation:** Handle invalid entries and common file-related errors.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3 | Application logic |
| `json` | Reading and writing persistent data |
| `csv` | Exporting expense records |
| `datetime` | Handling dates and monthly filtering |
| `pathlib` | Managing file paths |
| `abc` | Defining abstract classes and methods |
| Git | Version control |
| GitHub | Source code hosting |

The project uses Python's standard library and does not require third-party packages.

## 4. Project Structure

```text
Internova-Internship/
├── main.py
├── README.md
├── expenses.json
├── settings.json
├── expense_report.csv
├── Internship Report.docx
├── Internship Report.pdf
├── Internship Project Presentation.pptx
└── Outputs/
    └── Screenshots of application output
```

**Note:** The structure above is the intended final organization. Keep only files that actually exist in the repository, and include the PDF and presentation if they are part of your submission.

### Important Files

- `main.py` — Contains the application logic.
- `expenses.json` — Stores expense records.
- `settings.json` — Stores monthly budget settings.
- `expense_report.csv` — Generated when the CSV export feature is used.
- `Outputs/` — Contains screenshots demonstrating the project.
- `Internship Report.docx` — Editable project report.
- `Internship Report.pdf` — Final report in PDF format.
- `Internship Project Presentation.pptx` — Project presentation.

## 5. Python Concepts Demonstrated

- Variables, data types, operators, and type conversion
- Conditional statements and loops
- Functions and methods
- Lists and dictionaries
- File handling and JSON serialization
- CSV file generation
- Exception handling using `try` and `except`
- Classes, objects, and constructors
- Inheritance and encapsulation
- Abstraction and polymorphism
- Git and GitHub version control

## 6. Prerequisites

- Python 3 installed on your computer
- Visual Studio Code, Python IDLE, or another Python editor
- Git installed if you want to use version control

Download Python from: https://www.python.org/downloads/

## 7. Installation and Setup

### Step 1: Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/jeevaneshwar22-dev/Internova-Internship.git
```

### Step 2: Open the Project Folder

```bash
cd Internova-Internship
```

### Step 3: Check Python Installation

```bash
python --version
```

On Windows, you can also use:

```bash
py --version
```

### Step 4: Run the Application

```bash
python main.py
```

On Windows, you can also use:

```bash
py main.py
```

No additional package installation should be necessary when the application uses only Python's standard library.

## 8. How to Use the Application

When the application starts, a menu is displayed in the terminal.

| Option | Operation |
|---|---|
| 1 | Add Expense |
| 2 | View All Expenses |
| 3 | Search Expenses |
| 4 | Delete Expense |
| 5 | Set Monthly Budget |
| 6 | View Monthly Budget |
| 7 | Generate Expense Report |
| 8 | Export Report to CSV |
| 9 | Exit |

Select the required option and follow the instructions displayed by the program.

The application should save expense records and budget settings to their respective JSON files. The CSV report should be generated when the export option is selected.

## 9. Data Storage

The application uses local files to retain information between sessions.

- **`expenses.json`** stores expense records.
- **`settings.json`** stores budget settings.
- **`expense_report.csv`** contains the exported expense records after a successful CSV export.

Keep the JSON files in the expected project directory. Back up important data before manually editing or deleting these files.

## 10. Screenshots and Outputs

The `Outputs/` directory contains screenshots demonstrating the application's interface and operations.

Recommended screenshots include:

1. Main menu
2. Adding an expense
3. Viewing all expenses
4. Searching expenses
5. Setting and viewing the monthly budget
6. Generating an expense report
7. Exporting expenses to CSV
8. Git commands and successful repository upload

Use genuine screenshots from the final tested version of the application.

## 11. Future Improvements

- Graphical user interface using Tkinter
- Web application using Flask or Django
- Database integration using SQLite or MySQL
- Expense charts and visual analytics
- Expense editing functionality
- Budget alerts and category-wise limits
- Automated unit testing
- PDF report generation
- User authentication for a multi-user version

## 12. Conclusion

The Student Expense Tracker and Budget Management System is designed to help students organize expense records, monitor monthly spending, and manage a budget through a simple Python interface.

The project provides practical experience with Python programming, file handling, data structures, exception handling, object-oriented programming, and version control using Git and GitHub.

**Project Type:** Python Final Internship Project  
**Domain:** Personal Finance and Expense Management  
**Repository:** https://github.com/jeevaneshwar22-dev/Internova-Internship
