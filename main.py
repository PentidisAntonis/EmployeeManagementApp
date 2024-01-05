import sqlite3

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox

import sys
from PyQt6.QtGui import QAction
import sqlite3


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

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM employee") # it is a list of tuples so, we have to use to for
        self.table.setRowCount(0)        # This will ensure that the data will not be saved on top of the others
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()



app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
