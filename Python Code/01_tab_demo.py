import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget


class MyWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(" Demo for 2/17/2026")
        self.main

    pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
