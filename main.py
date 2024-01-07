import sqlite3

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget,  QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox

import sys
from PyQt6.QtGui import QAction
import sqlite3


def insert():
    dialog = InsertDialog()
    dialog.exec()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Management System")

        file_menu_item = self.menuBar().addMenu("&File")
        # self refers to MainWindow class and menuBar comes from QMainWindow the parent of "MainWindow(QMainWindow)"
        help_menu_item = self.menuBar().addMenu("&Help")

        add_employee_action = QAction("Add Employee", self)
        # sub item of file_menu_item, QAction is a class, self will connect this QAction
        # to the actual class MainWindow
        file_menu_item.addAction(add_employee_action)
        # This "addAction" is a method of file_menu_item, this action gets as input a QAction input the
        # add_employee_action

        about_action = QAction("About")
        help_menu_item.addAction(about_action)
        # about_action.setMenuRole(QAction.MenuRole.NoRole) #only for macbook if it doesnt show the about_action

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Department", "Mobile"))
        self.setCentralWidget(self.table)
        # when we use a QMainWindow we have to set a central widget because we have menu bar and tool bar
        add_employee_action.triggered.connect(self.insert)  # connect to the insert method

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM employees")  # it is a list of tuples so, we have to use to for
        self.table.setRowCount(0)        # This will ensure that the data will not be saved on top of the others

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                local_item = QTableWidgetItem(str(data))
                local_item.setFlags(local_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make the item read-only
                self.table.setItem(row_number, column_number, local_item)
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Insert Employee Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add employee name widget
        self.employee_name = QLineEdit()
        self.employee_name.setPlaceholderText("Name")
        layout.addWidget(self.employee_name)

        # Add combo box of Departments
        self.department_name = QComboBox()
        departments = ["IT", "HR", "Marketing", "Sales"]
        self.department_name.addItems(departments)
        layout.addWidget(self.department_name)

        # Add mobile widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Add submit button
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
        main_window.load_data()  # load the new employee


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()  # Call load_data to populate the table initially
sys.exit(app.exec())
