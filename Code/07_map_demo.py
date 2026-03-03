import sys

import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

# Globals

cctv_df: pd.DataFrame
STARTTIME: int = 0
FINISHTIME: int = 23


class MapPage(QWidget):
    MAP_IMAGE_SIZE = int(885 / 3)

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
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
        dayDropMenu.currentIndexChanged.connect(self.on_day_changed)

        # Season Menu
        seasonDropMenu = QComboBox()
        seasonDropMenu.addItems(["Winter", "Spring", "Summer", "Autumn"])
        seasonDropMenu.currentIndexChanged.connect(self.on_season_changed)

        # Start time container
        startTimeContainer = QVBoxLayout()
        startTimeContainer.setSpacing(0)

        # Start time label
        self.startTimeLabel = QLabel("Start Time: " + str(STARTTIME))

        # Start time slider
        startTimeSlider = QSlider()
        startTimeSlider.setMaximum(23)
        startTimeSlider.setMinimum(0)
        startTimeSlider.setOrientation(Qt.Orientation.Horizontal)
        startTimeSlider.valueChanged.connect(self.on_start_time_changed)

        startTimeContainer.addWidget(self.startTimeLabel)
        startTimeContainer.addWidget(startTimeSlider)

        # Finish time container
        finishTimeContainer = QVBoxLayout()
        finishTimeContainer.setSpacing(0)

        # Finish time label
        self.finishTimeLabel = QLabel("Finish Time: " + str(FINISHTIME))

        # Finish time slider
        finishTimeSlider = QSlider()
        finishTimeSlider.setMaximum(23)
        finishTimeSlider.setMinimum(0)
        finishTimeSlider.setOrientation(Qt.Orientation.Horizontal)
        finishTimeSlider.valueChanged.connect(self.on_finish_time_changed)

        finishTimeContainer.addWidget(self.finishTimeLabel)
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
        camerasContainer = QHBoxLayout()

        self.checkbox_308 = QCheckBox("308 Murraygate")
        self.checkbox_310 = QCheckBox("310 Seagate")
        self.checkbox_317 = QCheckBox("317 Reform St")
        self.checkbox_320 = QCheckBox("320 Westport")
        self.checkbox_323 = QCheckBox("323 Union Street")
        self.checkbox_328 = QCheckBox("328 South Marketgate")
        self.checkbox_332 = QCheckBox("332 Waterfront")
        self.checkbox_500 = QCheckBox("500 Hilltown")

        self.checkbox_308.stateChanged.connect(self.on_camera_changed)
        self.checkbox_310.stateChanged.connect(self.on_camera_changed)
        self.checkbox_317.stateChanged.connect(self.on_camera_changed)
        self.checkbox_320.stateChanged.connect(self.on_camera_changed)
        self.checkbox_323.stateChanged.connect(self.on_camera_changed)
        self.checkbox_328.stateChanged.connect(self.on_camera_changed)
        self.checkbox_332.stateChanged.connect(self.on_camera_changed)
        self.checkbox_500.stateChanged.connect(self.on_camera_changed)

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
        gridLayout = QGridLayout()

        # 308 Murraygate
        pixmap_308 = QPixmap("../Data/MapImages/308_murraygate.png")
        scaledPixmap_308 = pixmap_308.scaled(
            MapPage.MAP_IMAGE_SIZE, MapPage.MAP_IMAGE_SIZE
        )
        label_308 = QLabel("308 Murraygate")
        label_308.setPixmap(scaledPixmap_308)

        gridLayout.addWidget(label_308, 0, 0)

        # 310 Seagate
        pixmap_310 = QPixmap("../Data/MapImages/310_seagate.png")
        scaledPixmap_310 = pixmap_310.scaled(
            MapPage.MAP_IMAGE_SIZE, MapPage.MAP_IMAGE_SIZE
        )
        label_310 = QLabel("310 Seagate")
        label_310.setPixmap(scaledPixmap_310)
        gridLayout.addWidget(label_310, 0, 1)

        # 317 Reform St
        pixmap_317 = QPixmap("../Data/MapImages/317_reform_st.png")
        scaledPixmap_317 = pixmap_317.scaled(
            MapPage.MAP_IMAGE_SIZE, MapPage.MAP_IMAGE_SIZE
        )
        label_317 = QLabel("317 Reform St")
        label_317.setPixmap(scaledPixmap_317)
        gridLayout.addWidget(label_317, 0, 2)

        # 320 Westport
        pixmap_320 = QPixmap("../Data/MapImages/320_westport.png")
        scaledPixmap_320 = pixmap_320.scaled(
            MapPage.MAP_IMAGE_SIZE, MapPage.MAP_IMAGE_SIZE
        )
        label_320 = QLabel("320 Westport")
        label_320.setPixmap(scaledPixmap_320)
        gridLayout.addWidget(label_320, 1, 0)

        # Dundee Overview
        pixmap_overview = QPixmap("../Data/MapImages/dundee_overview.png")
        scaledPixmap_overview = pixmap_overview.scaled(
            MapPage.MAP_IMAGE_SIZE, MapPage.MAP_IMAGE_SIZE
        )
        label_overview = QLabel("Dundee Overview")
        label_overview.setPixmap(scaledPixmap_overview)
        gridLayout.addWidget(label_overview, 1, 1)

        # 323 Union Street
        pixmap_323 = QPixmap("../Data/MapImages/323_union_street.png")
        scaledPixmap_323 = pixmap_323.scaled(
            MapPage.MAP_IMAGE_SIZE, MapPage.MAP_IMAGE_SIZE
        )
        label_323 = QLabel("323 Union Street")
        label_323.setPixmap(scaledPixmap_323)
        gridLayout.addWidget(label_323, 1, 2)

        # 328 South Marketgate
        pixmap_328 = QPixmap("../Data/MapImages/328_south_marketgate.png")
        scaledPixmap_328 = pixmap_328.scaled(
            MapPage.MAP_IMAGE_SIZE, MapPage.MAP_IMAGE_SIZE
        )
        label_328 = QLabel("328 South Marketgate")
        label_328.setPixmap(scaledPixmap_328)
        gridLayout.addWidget(label_328, 2, 0)

        # 332 Waterfront
        pixmap_332 = QPixmap("../Data/MapImages/332_waterfront.png")
        scaledPixmap_332 = pixmap_332.scaled(
            MapPage.MAP_IMAGE_SIZE, MapPage.MAP_IMAGE_SIZE
        )
        label_332 = QLabel("332 Waterfront")
        label_332.setPixmap(scaledPixmap_332)
        gridLayout.addWidget(label_332, 2, 1)

        # 500 Hilltown
        pixmap_500 = QPixmap("../Data/MapImages/500_hilltown.png")
        scaledPixmap_500 = pixmap_500.scaled(
            MapPage.MAP_IMAGE_SIZE, MapPage.MAP_IMAGE_SIZE
        )
        label_500 = QLabel("500 Hilltown")
        label_500.setPixmap(scaledPixmap_500)
        gridLayout.addWidget(label_500, 2, 2)

        mapTopBar.addWidget(dayDropMenu)
        mapTopBar.addWidget(seasonDropMenu)
        mapTopBar.addLayout(startTimeContainer)
        mapTopBar.addLayout(finishTimeContainer)
        layout.addLayout(mapTopBar)
        layout.addLayout(camerasContainer)
        layout.addLayout(gridLayout)
        self.setLayout(layout)

    def apply_tint(self, pixmap: QPixmap, color: QColor) -> QPixmap:
        # Create a copy to work on
        tinted = pixmap.copy()
        painter = QPainter(tinted)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        painter.fillRect(tinted.rect(), color)
        painter.end()
        return tinted

    def on_day_changed(self, index):
        pass

    def on_season_changed(self, index):
        pass

    def on_start_time_changed(self, value):
        STARTTIME = value
        self.startTimeLabel.setText("Start Time: " + str(STARTTIME))

    def on_finish_time_changed(self, value):
        FINISHTIME = value
        self.finishTimeLabel.setText("Start Time: " + str(FINISHTIME))

    def on_camera_changed(self, state):
        self.sender()
        pass

    def updateData(self):
        pass


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
        self.loadData()

    def loadData(self):
        cctv_df = pd.read_csv("../Data/Processed/05_Human_Readable.csv")

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
