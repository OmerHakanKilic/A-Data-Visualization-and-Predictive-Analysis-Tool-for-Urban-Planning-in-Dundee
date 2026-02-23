import sys

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


class MapPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        mapTopBar = QHBoxLayout()
        mapTopBar.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Drop Menu
        dayDropMenu = QComboBox()
        dayDropMenu.addItems(
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
        )

        # Season Menu
        seasonDropMenu = QComboBox()
        seasonDropMenu.addItems(["Winter", "Spring", "Summer", "Autumn"])

        # Start time container
        startTimeContainer = QVBoxLayout()
        startTimeContainer.setSpacing(0)

        # Start time label
        startTimeLabel = QLabel("Start Time")

        # Start time slider
        startTimeSlider = QSlider()
        startTimeSlider.setMaximum(23)
        startTimeSlider.setMinimum(0)
        startTimeSlider.setOrientation(Qt.Orientation.Horizontal)

        startTimeContainer.addWidget(startTimeLabel)
        startTimeContainer.addWidget(startTimeSlider)

        # Finish time container
        finishTimeContainer = QVBoxLayout()
        finishTimeContainer.setSpacing(0)

        # Finish time label
        finishTimeLabel = QLabel("Finish Time")

        # Finish time slider
        finishTimeSlider = QSlider()
        finishTimeSlider.setMaximum(23)
        finishTimeSlider.setMinimum(0)
        finishTimeSlider.setOrientation(Qt.Orientation.Horizontal)

        finishTimeContainer.addWidget(finishTimeLabel)
        finishTimeContainer.addWidget(finishTimeSlider)

        """
        Sources list:
        317 Reform St
        500 Hilltown
        308 Murraygate
        328 South Marketgate
        310 Seagate
        323 Union Street
        320 Westport
        332 Waterfront
        """
        # Sources container
        camerasContainer = QVBoxLayout()

        self.checkbox_308 = QCheckBox("308 Murraygate")
        self.checkbox_310 = QCheckBox("310 Seagate")
        self.checkbox_317 = QCheckBox("317 Reform St")
        self.checkbox_320 = QCheckBox("320 Westport")
        self.checkbox_323 = QCheckBox("323 Union Street")
        self.checkbox_328 = QCheckBox("328 South Marketgate")
        self.checkbox_332 = QCheckBox("332 Waterfront")
        self.checkbox_500 = QCheckBox("500 Hilltown")

        # Adding them to the specific container
        camerasContainer.addWidget(self.checkbox_308)
        camerasContainer.addWidget(self.checkbox_310)
        camerasContainer.addWidget(self.checkbox_317)
        camerasContainer.addWidget(self.checkbox_320)
        camerasContainer.addWidget(self.checkbox_323)
        camerasContainer.addWidget(self.checkbox_328)
        camerasContainer.addWidget(self.checkbox_332)
        camerasContainer.addWidget(self.checkbox_500)

        # Embedded map
        self.browser = QWebEngineView()
        map_url = "https://uod.maps.arcgis.com/apps/mapviewer/index.html?webmap=c697947abbf441159a34e08b1f8d31e5"
        self.browser.setUrl(QUrl(map_url))

        mapTopBar.addWidget(dayDropMenu)
        mapTopBar.addWidget(seasonDropMenu)
        mapTopBar.addLayout(startTimeContainer)
        mapTopBar.addLayout(finishTimeContainer)
        layout.addLayout(mapTopBar)
        layout.addLayout(camerasContainer)
        layout.addWidget(self.browser)
        self.setLayout(layout)


class MLPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("ML Page"))
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 1000, 1000)
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

        self.stack.setCurrentIndex(1)

        self.homeButton.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.machineButton.clicked.connect(lambda: self.stack.setCurrentIndex(0))

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
