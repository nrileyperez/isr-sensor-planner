from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.scenario import Scenario

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QDoubleSpinBox,
    QPushButton,
    QGroupBox,
)

class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        sensor_group = QGroupBox("Sensor Settings")
        sensor_layout = QFormLayout()

        self.x_spin = QDoubleSpinBox()
        self.x_spin.setRange(0, 100000)
        self.x_spin.setValue(2030)

        self.y_spin = QDoubleSpinBox()
        self.y_spin.setRange(0, 100000)
        self.y_spin.setValue(1925)

        self.height_spin = QDoubleSpinBox()
        self.height_spin.setRange(0, 10000)
        self.height_spin.setValue(300)

        self.azimuth_spin = QDoubleSpinBox()
        self.azimuth_spin.setRange(0, 360)
        self.azimuth_spin.setValue(160)

        self.tilt_spin = QDoubleSpinBox()
        self.tilt_spin.setRange(-90, 90)
        self.tilt_spin.setValue(10)

        self.fov_spin = QDoubleSpinBox()
        self.fov_spin.setRange(1, 180)
        self.fov_spin.setValue(75)

        self.range_spin = QDoubleSpinBox()
        self.range_spin.setRange(1, 100000)
        self.range_spin.setValue(8455)

        sensor_layout.addRow("X Position", self.x_spin)
        sensor_layout.addRow("Y Position", self.y_spin)
        sensor_layout.addRow("Height", self.height_spin)
        sensor_layout.addRow("Azimuth", self.azimuth_spin)
        sensor_layout.addRow("Tilt", self.tilt_spin)
        sensor_layout.addRow("Field of View", self.fov_spin)
        sensor_layout.addRow("Max Range", self.range_spin)

        sensor_group.setLayout(sensor_layout)

        self.sim_button = QPushButton("Simulate Coverage")

        metrics_group = QGroupBox("Summary")
        metrics_layout = QVBoxLayout()
        self.visible_label = QLabel("Visible Area: 47,250 m²")
        self.blocked_label = QLabel("Blocked Area: 31,440 m²")
        self.distance_label = QLabel("Max Visible Distance: 8455 m")
        metrics_layout.addWidget(self.visible_label)
        metrics_layout.addWidget(self.blocked_label)
        metrics_layout.addWidget(self.distance_label)
        metrics_group.setLayout(metrics_layout)

        main_layout.addWidget(sensor_group)
        main_layout.addWidget(self.sim_button)
        main_layout.addWidget(metrics_group)
        main_layout.addStretch()

    def set_from_scenario(self, scenario: "Scenario") -> None:
        self.x_spin.setValue(scenario.sensor_x)
        self.y_spin.setValue(scenario.sensor_y)
        self.height_spin.setValue(scenario.sensor_height)
        self.azimuth_spin.setValue(scenario.azimuth)
        self.tilt_spin.setValue(scenario.tilt)
        self.fov_spin.setValue(scenario.field_of_view)
        self.range_spin.setValue(scenario.max_range)

    def get_sensor_values(self) -> dict[str, float]:
        """Return the current sensor-related values from the UI widgets."""
        return {
            "sensor_x": self.x_spin.value(),
            "sensor_y": self.y_spin.value(),
            "sensor_height": self.height_spin.value(),
            "azimuth": self.azimuth_spin.value(),
            "tilt": self.tilt_spin.value(),
            "field_of_view": self.fov_spin.value(),
            "max_range": self.range_spin.value(),
        }