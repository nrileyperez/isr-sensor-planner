from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QToolBar,
)

from app.ui.control_panel import ControlPanel
from app.ui.layer_panel import LayerPanel
from app.ui.status_panel import StatusPanel
from app.ui.terrain_view import TerrainView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ISR Sensor Coverage Planner")
        self.resize(1500, 900)

        self._create_toolbar()
        self._create_central_layout()

    def _create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        load_action = QAction("Load Terrain", self)
        reset_action = QAction("Reset", self)
        save_action = QAction("Save Scenario", self)

        load_action.triggered.connect(self.on_load_terrain)
        reset_action.triggered.connect(self.on_reset)
        save_action.triggered.connect(self.on_save_scenario)

        toolbar.addAction(load_action)
        toolbar.addAction(reset_action)
        toolbar.addAction(save_action)

    def _create_central_layout(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        outer_layout = QVBoxLayout()
        central_widget.setLayout(outer_layout)

        middle_layout = QHBoxLayout()

        self.control_panel = ControlPanel()
        self.terrain_view = TerrainView()
        self.layer_panel = LayerPanel()
        self.status_panel = StatusPanel()

        self.control_panel.setMinimumWidth(280)
        self.layer_panel.setMinimumWidth(220)

        middle_layout.addWidget(self.control_panel, 0)
        middle_layout.addWidget(self.terrain_view, 1)
        middle_layout.addWidget(self.layer_panel, 0)

        outer_layout.addLayout(middle_layout, 1)
        outer_layout.addWidget(self.status_panel, 0)

    def on_load_terrain(self):
        print("Load Terrain clicked")

    def on_reset(self):
        print("Reset clicked")

    def on_save_scenario(self):
        print("Save Scenario clicked")