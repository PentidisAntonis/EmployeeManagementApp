from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget

import sys
from PyQt6.QtGui import QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Management System")

        file_menu_item = self.menuBar().addMenu("&File")
        # self refers to MainWindow class and menuBar comes from QMainWindow the parent of "MainWindow(QMainWindow)"
        help_menu_item = self.menuBar().addMenu("&Help")

        add_employee_action = QAction("Add Employee", self)
        # sub item of file_menu_item, QAction is a class, self will connect this QAction to the actual class MainWindow
        file_menu_item.addAction(add_employee_action)
        # This "addAction" is a method of file_menu_item, this action gets as input a QAction input the
        # add_employee_action

        about_action = QAction("About")
        help_menu_item.addAction(about_action)
    # about_action.setMenuRole(QAction.MenuRole.NoRole) 	#only for macbook if it doesnt show the about_action

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Department", "Mobile"))
        self.setCentralWidget(self.table)
        # when we use a QMainWindow we have to set a central widget because we have menu bar and tool bar

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
