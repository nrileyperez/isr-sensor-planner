from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QToolBar,
)

from app.models.scenario import Scenario
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

        self.scenario = Scenario()

        self.control_panel.set_from_scenario(self.scenario)
        self.terrain_view.set_scenario(self.scenario)
        self._connect_control_signals()

        # Force one initial UI -> scenario sync so later updates use a known-good state.
        self.on_sensor_controls_changed()
    
    def _connect_control_signals(self):
        self.control_panel.x_spin.valueChanged.connect(self.on_sensor_controls_changed)
        self.control_panel.y_spin.valueChanged.connect(self.on_sensor_controls_changed)
        self.control_panel.height_spin.valueChanged.connect(self.on_sensor_controls_changed)
        self.control_panel.azimuth_spin.valueChanged.connect(self.on_sensor_controls_changed)
        self.control_panel.tilt_spin.valueChanged.connect(self.on_sensor_controls_changed)
        self.control_panel.fov_spin.valueChanged.connect(self.on_sensor_controls_changed)
        self.control_panel.range_spin.valueChanged.connect(self.on_sensor_controls_changed)

    def on_sensor_controls_changed(self, *_args):
        values = self.control_panel.get_sensor_values()

        # Update scenario state from the UI controls.
        self.scenario.sensor_x = values["sensor_x"]
        self.scenario.sensor_y = values["sensor_y"]
        self.scenario.sensor_height = values["sensor_height"]
        self.scenario.azimuth = values["azimuth"]
        self.scenario.tilt = values["tilt"]
        self.scenario.field_of_view = values["field_of_view"]
        self.scenario.max_range = values["max_range"]

        print(
            "sensor controls changed -> "
            f"x={self.scenario.sensor_x:.1f}, "
            f"y={self.scenario.sensor_y:.1f}, "
            f"height={self.scenario.sensor_height:.1f}"
        )

        # Redraw the marker if the terrain view has the update hook.
        if hasattr(self.terrain_view, "update_sensor_marker"):
            self.terrain_view.update_sensor_marker()

        self.status_panel.coords_label.setText(
            f"Coords: ({self.scenario.sensor_x:.1f}, {self.scenario.sensor_y:.1f})"
        )
        self.status_panel.distance_label.setText(
            f"Max Visible Distance: {self.scenario.max_range:.1f} m"
        )

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