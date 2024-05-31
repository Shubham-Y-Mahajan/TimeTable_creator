from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QIcon, QColor
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QComboBox, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QToolBar, QStatusBar, QMessageBox
import sys


class LoginWindow(QMainWindow):


    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(500, 500)  # min window size

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)

        swap_button = QPushButton("Swap Screen")
        swap_button.clicked.connect(self.swap_screen)

        layout.addWidget(swap_button, 1, 1)
    def swap_screen(self):
        self.close()
        self.signup_window= SignUpWindow()
        self.signup_window.show()


class SignUpWindow(QMainWindow):


    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign Up")
        self.setFixedSize(500, 500)  # min window size

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)

        back_button = QPushButton("Go Back")
        back_button.clicked.connect(self.back)

        layout.addWidget(back_button, 1, 1)

    def back(self):
        self.login_window=LoginWindow()
        self.login_window.show()
        self.close()


app = QApplication(sys.argv)

login_window = LoginWindow()




login_window.show()

sys.exit(app.exec())
