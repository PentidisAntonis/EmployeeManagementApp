import sqlite3
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox

import sys
from PyQt6.QtGui import QAction

def insert():
    dialog = InsertDialog()
    dialog.exec()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Management System")
        self.setFixedWidth(410)
        self.setFixedHeight(400)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        add_employee_action = QAction("Add Employee", self)
        file_menu_item.addAction(add_employee_action)

        search_employee_action = QAction("Search Employee", self)
        file_menu_item.addAction(search_employee_action)
        search_employee_action.triggered.connect(self.show_search_dialog)

        show_all_action = QAction("Show All Employees", self)
        file_menu_item.addAction(show_all_action)
        show_all_action.triggered.connect(self.load_data)  # Connect to the method that loads all employees

        about_action = QAction("About")
        help_menu_item.addAction(about_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Department", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        add_employee_action.triggered.connect(self.insert)
        self.load_data()

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM employees")
        self.table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                if column_number != 0:  # Skip making the 'Id' column editable
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row_number, column_number, item)

        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def show_search_dialog(self):
        dialog = SearchDialog()
        dialog.exec()

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Insert Employee Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.employee_name = QLineEdit()
        self.employee_name.setPlaceholderText("Name")
        layout.addWidget(self.employee_name)

        self.department_name = QComboBox()
        departments = ["IT", "HR", "Marketing", "Sales"]
        self.department_name.addItems(departments)
        layout.addWidget(self.department_name)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        button = QPushButton("Register")
        button.clicked.connect(self.add_employee)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_employee(self):
        name = self.employee_name.text()
        department = self.department_name.itemText(self.department_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO employees (name, department, mobile) VALUES (?, ?, ?)",
                       (name, department, mobile))

        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Employee")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Create layout and input widget
        layout = QVBoxLayout()

        self.employee_name = QLineEdit()
        self.employee_name.setPlaceholderText("Name")
        layout.addWidget(self.employee_name)

        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        name = self.employee_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM employees WHERE name=?", (name,))
        row = list(result)
        # Clear the existing contents of the table
        main_window.table.clearContents()
        main_window.table.setRowCount(0)

        for row_number, row_data in enumerate(row):
            main_window.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                if column_number != 0:  # Skip making the 'Id' column editable
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                main_window.table.setItem(row_number, column_number, item)

        cursor.close()
        connection.close()

        # Close the dialog
        self.accept()

    def show_all_employees(self):
        # Clear the text in the search input
        self.employee_name.clear()

        # Call the search method to reload all employees
        self.search()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
