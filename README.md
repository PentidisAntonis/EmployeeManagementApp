**Employee Management System**

This simple Employee Management System is a PyQt6-based application with SQLite as the underlying database. It provides basic functionalities for managing employee data, including adding, editing, deleting, searching, and viewing all employees.

**Prerequisites**

Before running the application, ensure you have Python and PyQt6 installed. You can install PyQt6 using the following command:

>pip install PyQt6


**Running the Application**

Execute the following command in your terminal to run the Employee Management System:

python main.py

**Features**

**Main Window:**

Displays a table with employee information, including columns for ID, Name, Department, and Mobile.
Provides a top toolbar with options to add, edit, and view all employees.
File menu includes actions for adding employees and showing all employees.
Edit menu includes a search action.

**Add Employee:**

Opens a dialog for inserting new employee data.
Requires entering the employee's name, selecting a department, and providing a mobile number.

**Edit Employee:**

Opens a dialog for updating existing employee data.
Retrieves current data from the selected row in the main window table.
Allows modifying the employee's name, department, and mobile number.

**Delete Employee:**

Opens a dialog to confirm the deletion of an employee record.
Deletes the selected employee record from the database.

**Search Employee:**

Opens a dialog for searching employees by name.
Displays matching results in the main window table.

**About Dialog:**

Provides information about the purpose of the application.

**Database Connection**

The DatabaseConnection class manages the SQLite database connection. By default, the database file is named "database.db."

**Additional Information**

Icons used for actions are expected to be in the same directory as the script (add.png, pencil.png, employees.png, search.png).
The application uses a simple SQLite database named "database.db" to store employee information.

**Downloading SQLite:**

SQLite comes bundled with Python, but if you need a standalone installation for development or administration purposes, you can download the command-line shell from the SQLite website.

Visit the SQLite Download Page:
Go to the SQLite download page at sqlite.org/download.html.

