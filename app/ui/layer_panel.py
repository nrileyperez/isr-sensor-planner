from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QGroupBox


class LayerPanel(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        layers_group = QGroupBox("Coverage Layers")
        layers_layout = QVBoxLayout()

        self.terrain_checkbox = QCheckBox("Terrain Mesh")
        self.terrain_checkbox.setChecked(True)

        self.sensor_checkbox = QCheckBox("Sensor Cone")
        self.sensor_checkbox.setChecked(True)

        self.los_checkbox = QCheckBox("Line of Sight")
        self.los_checkbox.setChecked(True)

        self.visible_checkbox = QCheckBox("Visible Area")
        self.visible_checkbox.setChecked(True)

        self.occlusion_checkbox = QCheckBox("Occlusion Mask")
        self.occlusion_checkbox.setChecked(True)

        layers_layout.addWidget(self.terrain_checkbox)
        layers_layout.addWidget(self.sensor_checkbox)
        layers_layout.addWidget(self.los_checkbox)
        layers_layout.addWidget(self.visible_checkbox)
        layers_layout.addWidget(self.occlusion_checkbox)

        layers_group.setLayout(layers_layout)

        main_layout.addWidget(layers_group)
        main_layout.addStretch()