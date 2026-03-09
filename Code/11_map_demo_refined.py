import sys

import pandas as pd
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QSlider,
    QSplitter,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

# Globals

cctv_df: pd.DataFrame
STATE = {
    "startTime": 0,
    "finishTime": 23,
    "day": "Monday",
    "season": "All",
    "Camera": "308 Murraygate",
}


class MapPage(QWidget):
    MAP_IMAGE_SIZE = int(885 / 3)
    sidebar_hidden = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        mainSplitter = QSplitter(Qt.Orientation.Horizontal)

        sidebarLayout = QVBoxLayout()
        sidebarLayout.setSpacing(10)
        sidebarLayout.setContentsMargins(10, 10, 10, 10)

        headerLayout = QHBoxLayout()
        headerLayout.addStretch()
        closeSidebarBtn = QPushButton("✕")
        closeSidebarBtn.setFixedSize(30, 30)
        closeSidebarBtn.clicked.connect(self.hide_sidebar)
        headerLayout.addWidget(closeSidebarBtn)

        sidebarLayout.addLayout(headerLayout)

        filtersLabel = QLabel("Filters")
        filtersLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        sidebarLayout.addWidget(filtersLabel)

        dayLabel = QLabel("Day:")
        self.dayDropMenu = QComboBox()
        self.dayDropMenu.addItems(
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
        self.dayDropMenu.currentIndexChanged.connect(self.on_day_changed)

        seasonLabel = QLabel("Season:")
        self.seasonDropMenu = QComboBox()
        self.seasonDropMenu.addItems(["Winter", "Spring", "Summer", "Autumn"])
        self.seasonDropMenu.currentIndexChanged.connect(self.on_season_changed)

        self.startTimeLabel = QLabel("Start Time: " + str(STATE["startTime"]))
        startTimeSlider = QSlider()
        startTimeSlider.setMaximum(23)
        startTimeSlider.setMinimum(0)
        startTimeSlider.setOrientation(Qt.Orientation.Horizontal)
        startTimeSlider.valueChanged.connect(self.on_start_time_changed)

        self.finishTimeLabel = QLabel("Finish Time: " + str(STATE["finishTime"]))
        finishTimeSlider = QSlider()
        finishTimeSlider.setMaximum(23)
        finishTimeSlider.setMinimum(0)
        finishTimeSlider.setOrientation(Qt.Orientation.Horizontal)
        finishTimeSlider.valueChanged.connect(self.on_finish_time_changed)

        camerasLabel = QLabel("Cameras:")
        camerasLabel.setStyleSheet(
            "font-weight: bold; font-size: 14px; margin-top: 10px;"
        )
        self.cameraComboBox = QComboBox()
        self.cameraComboBox.setMaxVisibleItems(8)

        camera_ids = [
            "308 Murraygate",
            "310 Seagate",
            "317 Reform St",
            "320 Westport",
            "323 Union Street",
            "328 South Marketgate",
            "332 Waterfront",
            "500 Hilltown",
        ]
        self.cameraComboBox.addItems(camera_ids)
        self.cameraComboBox.currentIndexChanged.connect(self.on_camera_changed)

        sidebarLayout.addWidget(dayLabel)
        sidebarLayout.addWidget(self.dayDropMenu)
        sidebarLayout.addWidget(seasonLabel)
        sidebarLayout.addWidget(self.seasonDropMenu)
        sidebarLayout.addWidget(self.startTimeLabel)
        sidebarLayout.addWidget(startTimeSlider)
        sidebarLayout.addWidget(self.finishTimeLabel)
        sidebarLayout.addWidget(finishTimeSlider)
        sidebarLayout.addWidget(camerasLabel)
        sidebarLayout.addWidget(self.cameraComboBox)
        sidebarLayout.addStretch()

        self.sidebarWidget = QWidget()
        self.sidebarWidget.setLayout(sidebarLayout)
        self.sidebarWidget.setFixedWidth(220)

        gridLayout = QGridLayout()

        placeholderLabel = QLabel("Map view will be implemented here")
        placeholderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        mapWidget = QWidget()
        mapWidget.setLayout(gridLayout)

        mainSplitter.addWidget(self.sidebarWidget)
        mainSplitter.addWidget(placeholderLabel)
        mainSplitter.setStretchFactor(0, 0)
        mainSplitter.setStretchFactor(1, 1)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(mainSplitter)
        self.setLayout(mainLayout)

    def apply_tint(self, pixmap: QPixmap, color: QColor) -> QPixmap:
        # Create a copy to work on
        tinted = pixmap.copy()
        painter = QPainter(tinted)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        painter.fillRect(tinted.rect(), color)
        painter.end()
        return tinted

    def on_day_changed(self, index):
        day_dict = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday",
        }
        STATE["day"] = day_dict[index]

    def on_season_changed(self, index):
        season_dict = {
            0: "Winter",
            1: "Spring",
            2: "Summer",
            3: "Autumn",
        }
        STATE["season"] = season_dict[index]

    def on_start_time_changed(self, value):
        STARTTIME = value
        self.startTimeLabel.setText("Start Time: " + str(STARTTIME))

    def on_finish_time_changed(self, value):
        FINISHTIME = value
        self.finishTimeLabel.setText("Start Time: " + str(FINISHTIME))

    def on_camera_clicked(self, item):
        pass

    def hide_sidebar(self):
        self.sidebarWidget.hide()
        self.sidebar_hidden.emit()

    def show_sidebar(self):
        self.sidebarWidget.show()

    def on_camera_changed(self, index):
        camera_dict = {
            0: "308 Murraygate",
            1: "310 Seagate",
            2: "317 Reform St",
            3: "320 Westport",
            4: "323 Union Street",
            5: "328 South Marketgate",
            6: "332 Waterfront",
            7: "500 Hilltown",
        }
        STATE["Camera"] = camera_dict[index]

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

        self.showSidebarBtn = QPushButton("☰", self)
        self.showSidebarBtn.setFixedSize(40, 40)
        self.showSidebarBtn.hide()
        self.showSidebarBtn.clicked.connect(self.on_show_sidebar_clicked)
        self.mapPage.sidebar_hidden.connect(self.on_sidebar_hidden)

        masterLayout = QVBoxLayout()

        topBar = QHBoxLayout()
        topBar.addWidget(self.homeButton)
        topBar.addWidget(self.machineButton)

        masterLayout.addLayout(topBar)
        masterLayout.addWidget(self.stack)

        central_widget.setLayout(masterLayout)

        self.central_layout = masterLayout

    def on_sidebar_hidden(self):
        self.showSidebarBtn.show()
        self.showSidebarBtn.setGeometry(5, 80, 40, 40)

    def on_show_sidebar_clicked(self):
        self.mapPage.show_sidebar()
        self.showSidebarBtn.hide()


def main():
    cctv_df = pd.read_csv("../Data/Processed/06_With_Holidays.csv")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
