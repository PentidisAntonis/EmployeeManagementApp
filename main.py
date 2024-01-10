import sqlite3
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QLabel, QLineEdit, QPushButton, QMainWindow,
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox,
    QToolBar, QStatusBar, QMessageBox
)
import sys
from PyQt6.QtGui import QAction, QIcon


class DatabaseConnection:
    def __init__(self, database_file="database.db"):
        self.database_file = database_file

    def connect(self):
        connection = sqlite3.connect(self.database_file)
        return connection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Management System")
        self.setFixedWidth(800)
        self.setFixedHeight(600)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Top toolbar
        toolbar_top = QToolBar()
        toolbar_top.setMovable(False)
        self.addToolBar(toolbar_top)

        # Add Employee action
        add_employee_action = QAction(QIcon("add.png"), "Add Employee", self)
        add_employee_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_employee_action)

        # Edit Record action
        edit_employee_action = QAction(QIcon("pencil.png"), "Edit Record", self)
        edit_employee_action.triggered.connect(self.edit)
        toolbar_top.addAction(edit_employee_action)

        # Show All action
        show_all_action = QAction(QIcon("employees.png"), "Show All Employees", self)
        show_all_action.triggered.connect(self.load_data)  # Connect to the method that loads all employees
        file_menu_item.addAction(show_all_action)
        toolbar_top.addAction(show_all_action)  # Add show all action to the toolbar

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)

        search_action = QAction(QIcon("search.png"), "Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Department", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # create toolbar and add toolbar elements
        toolbar_top.addAction(add_employee_action)
        toolbar_top.addAction(search_action)

        # create status bar and add status bar elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell clicked
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.statusbar.findChildren(QPushButton)
        # cleaning the children because every time we click in a line it will produce 2 more buttons indefinitely
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def load_data(self):
        connection = DatabaseConnection().connect()
        result = connection.execute("SELECT * FROM employees")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    @staticmethod
    def insert():
        dialog = InsertDialog()
        dialog.exec()

    @staticmethod
    def search():
        dialog = SearchDialog()
        dialog.exec()

    @staticmethod
    def edit():
        dialog = EditDialog()
        dialog.exec()

    @staticmethod
    def delete():
        dialog = DeleteDialog()
        dialog.exec()

    @staticmethod
    def about():
        dialog = AboutDialog()
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")

        layout = QVBoxLayout()

        content = "This app was created for training purposes"
        label = QLabel(content)
        layout.addWidget(label)

        self.setText(content)


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Employee Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Get employee name from selected row
        index = main_window.table.currentRow()
        employee_name = main_window.table.item(index, 1).text()

        # Get id from selected row
        self.employee_id = main_window.table.item(index, 0).text()

        # Add employee name widget
        layout = QVBoxLayout()
        self.employee_name = QLineEdit(employee_name)
        self.employee_name.setPlaceholderText("Name")
        layout.addWidget(self.employee_name)

        # Add combo box of departments
        department_name = main_window.table.item(index, 2).text()
        self.department_name = QComboBox()
        departments = ["IT", "HR", "Marketing", "Sales"]
        self.department_name.addItems(departments)
        self.department_name.setCurrentText(department_name)
        layout.addWidget(self.department_name)

        # Add mobile widget
        mobile = main_window.table.item(index, 3).text()
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Add a submit button
        button = QPushButton("Update")
        button.clicked.connect(self.update_employee)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_employee(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE employees SET name = ?, department = ?, mobile = ? WHERE id = ?",
                       (self.employee_name.text(),
                        self.department_name.itemText(self.department_name.currentIndex()),
                        self.mobile.text(),
                        self.employee_id))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()

        # Close the dialog
        self.accept()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Employee Data")

        layout = QVBoxLayout()
        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation)
        layout.addWidget(yes)
        layout.addWidget(no)
        self.setLayout(layout)

        yes.clicked.connect(self.delete_employee)
        no.clicked.connect(self.close)  # Close the dialog when "No" is clicked

    def delete_employee(self):
        # Get selected row index and employee id
        index = main_window.table.currentRow()
        employee_id = main_window.table.item(index, 0).text()

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE from employees WHERE id= ?", (employee_id,))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()

        self.show_success_message()

        self.close()

    @staticmethod
    def show_success_message():
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully!")
        confirmation_widget.exec()
        confirmation_widget.setText("The record was deleted successfully!")


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Employee Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add employee name widget
        self.employee_name = QLineEdit()
        self.employee_name.setPlaceholderText("Name")
        layout.addWidget(self.employee_name)

        # Add combo box of departments
        self.department_name = QComboBox()
        departments = ["IT", "HR", "Marketing", "Sales"]
        self.department_name.addItems(departments)
        layout.addWidget(self.department_name)

        # Add mobile widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Add a submit button
        button = QPushButton("Register")
        button.clicked.connect(self.add_employee)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_employee(self):
        name = self.employee_name.text()
        department = self.department_name.itemText(self.department_name.currentIndex())
        mobile = self.mobile.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO employees (name, department, mobile) VALUES (?, ?, ?)",
                       (name, department, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        self.close()
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
        connection = DatabaseConnection().connect()
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


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
