import sys
import subprocess
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt6.uic import loadUi


class LibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("menu.ui", self)
        self.setWindowTitle("Library App")
        self.resize(400, 300)
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        button_width = 200

        buttons = [
            ("Member", self.open_member),
            ("Staff", self.open_staff),
            ("Book", self.open_book),
        ]

        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        for button_text, button_action in buttons:
            button = QPushButton(button_text)
            button.setFixedWidth(button_width)
            layout.addWidget(button)
            button.clicked.connect(button_action)

    def open_member(self):
        subprocess.call(["python3", "member.py"])

    def open_staff(self):
        subprocess.call(["python3", "staff.py"])

    def open_book(self):
        subprocess.call(["python3", "book.py"])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec())