"""

    buttons.append(("Report Generation",self.generate_reports))

    def generate_reports(self):
        self.reports_window = ReportsWindow(logged_in_user=self.logged_in_user)
        self.reports_window .back_to_homepage_signal.connect(self.show)
        self.reports_window .show()
        self.hide()


"""
import json

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QComboBox, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QToolBar, QStatusBar, QMessageBox, QStackedLayout, QCheckBox, \
    QGroupBox, QRadioButton, QButtonGroup
from PyQt6 import QtCore

from backend import ConfirmationWidgets
from database_routine import Users,Roles,ActionHistory
from styles import Styles


class ReportsWindow(QMainWindow):
    back_to_homepage_signal=pyqtSignal()
    def __init__(self,logged_in_user):
        super().__init__()
        self.logged_in_user=logged_in_user
        self.back_button_clicked=False

        self.bucket={}

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Generate Reports")
        self.setMinimumSize(700,700)
        self.showMaximized()

        back_button = QPushButton("Back To Homepage")
        back_button.setStyleSheet(Styles().dark_red_push_button())
        back_button.clicked.connect(self.back_to_homepage)

        self.table = QTableWidget()
        # Disable editing for the entire table
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(("Table Name","Description"))
        self.table.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: lightgray; color: black; font-weight: bold }")

        # Set width for a particular column
        self.table.setColumnWidth(0, 300)  # Set the width of the column
        self.table.setColumnWidth(1, 700)  # Set the width of the column

        self.table.verticalHeader().setVisible(False)
        self.load_table_names()

        self.bucket_table = QTableWidget()
        # Disable editing for the entire table
        self.bucket_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.bucket_table.setColumnCount(2)
        self.bucket_table.setHorizontalHeaderLabels(("Tables to be considered", "Columns Chosen"))
        self.bucket_table.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: lightgray; color: black; font-weight: bold }")

        # Set width for a particular column
        self.bucket_table.setColumnWidth(0, 300)  # Set the width of the column
        self.bucket_table.setColumnWidth(1, 700)  # Set the width of the column

        self.bucket_table.verticalHeader().setVisible(False)



        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        layout.addWidget(self.table)
        layout.addWidget(self.bucket_table)

        toolbar = QToolBar()
        toolbar.setStyleSheet("background-color: #0099cc; spacing: 20px;")  # Set toolbar background color
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addWidget(back_button)

        # Create stautus bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.table.cellClicked.connect(self.cell_clicked_table)
        self.bucket_table.cellClicked.connect(self.cell_clicked_bucket_table)

    def load_table_names(self):

        self.table.setRowCount(0)


        result = [["RMS_MPR","Stores the details of a Manpower Requisition"],
                  ["RMS_CANDIDATE","Stores the details of all the registered candidates"],
                  ["RMS_MPR_PARTICIPANTS","Stores the 'STAGE' , 'STATUS', and 'GRADE', of a candidate contesting for a job vacancy"],
                  ["RMS_RECRUITMENT_HISTORY","Stores the entire recruitment history (across all MPRs) of all the registered candidates"],
                  ["RMS_INTERVIEW","Stores the data related to all the interviews"],
                  ["RMS_JOINING","Stores the 'CV_ID' and the date of joining of a candidate who is about to join the company"],
                  ["RMS_ACTION_HISTORY","Log"]]

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            # This inserts an empty row in the window
            for column_number, data in enumerate(row_data):
                # row_data is a tuple where each element of tuple is a column item
                item = QTableWidgetItem(str(data))

                item.setBackground(QColor("antiquewhite"))
                item.setForeground(QColor("black"))  # Set text color to purple
                item.setToolTip(str(data))
                self.table.setItem(row_number, column_number, item)

    def load_bucket(self):
        self.bucket_table.setRowCount(0)

        result=[[table,self.bucket[table]] for table in self.bucket]

        for row_number, row_data in enumerate(result):
            self.bucket_table.insertRow(row_number)
            # This inserts an empty row in the window
            for column_number, data in enumerate(row_data):
                # row_data is a tuple where each element of tuple is a column item
                item = QTableWidgetItem(str(data))

                item.setBackground(QColor("lightcyan"))
                item.setForeground(QColor("black"))  # Set text color to purple
                item.setToolTip(str(data))
                self.bucket_table.setItem(row_number, column_number, item)


    def cell_clicked_table(self):
        add_button = QPushButton("Add table to the bucket")
        add_button.clicked.connect(self.add_table)
        add_button.setFixedSize(200, 50)
        add_button.setStyleSheet(Styles().blue_push_button())

        # the below steps were taken to avoid duplication of buttons when we click on multiple cells
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(add_button)

    def cell_clicked_bucket_table(self):
        remove_button = QPushButton("Remove table")
        remove_button.clicked.connect(self.remove_table)
        remove_button.setFixedSize(200, 50)
        remove_button.setStyleSheet(Styles().dark_red_push_button())

        # the below steps were taken to avoid duplication of buttons when we click on multiple cells
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(remove_button)

    def add_table(self):
        try:
            selected_row = self.table.currentRow()

            table_name=self.table.item(selected_row,0).text()

            if table_name not in self.bucket:
                self.bucket[table_name]=[]
                self.load_bucket()


        except AttributeError: # no user selected but button has been clicked
            ConfirmationWidgets().error(text="Kindly select a cell")

    def remove_table(self):
        try:
            selected_row = self.bucket_table.currentRow()

            table_name=self.bucket_table.item(selected_row,0).text()

            if table_name in self.bucket:
                del self.bucket[table_name]
                self.load_bucket()


        except AttributeError: # no user selected but button has been clicked
            ConfirmationWidgets().error(text="Kindly select a cell")


    def back_to_homepage(self):
        self.back_button_clicked=True
        self.back_to_homepage_signal.emit()
        self.close()


    def closeEvent(self, event):
        if not self.back_button_clicked: # means top right x was clicked
            Users().reset_login_flag(emp_code=self.logged_in_user)
        super().closeEvent(event)