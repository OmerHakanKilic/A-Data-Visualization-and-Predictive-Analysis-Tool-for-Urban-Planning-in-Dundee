import sys

from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


class MapPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h1>This is the Machine Learning Page</h1>"))
        self.setLayout(layout)


class MLPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h1>This is the Map Page</h1>"))
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 500, 500)
        self.stack = QStackedWidget()
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.homeButton = QPushButton("Home Tab")
        self.machineButton = QPushButton("Machine learning Tab")

        self.mapPage = MapPage()
        self.mlpage = MLPage()

        self.stack.addWidget(self.mlpage)
        self.stack.addWidget(self.mapPage)

        self.homeButton.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.machineButton.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        masterLayout = QVBoxLayout()

        topBar = QHBoxLayout()
        topBar.addWidget(self.homeButton)
        topBar.addWidget(self.machineButton)

        masterLayout.addLayout(topBar)
        masterLayout.addWidget(self.stack)

        central_widget.setLayout(masterLayout)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
