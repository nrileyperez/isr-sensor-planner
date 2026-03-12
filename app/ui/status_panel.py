from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame


class StatusPanel(QFrame):
    def __init__(self):
        super().__init__()

        self.setFrameShape(QFrame.StyledPanel)

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.visible_label = QLabel("Visible Area: 47,250 m²")
        self.blocked_label = QLabel("Blocked Area: 31,440 m²")
        self.distance_label = QLabel("Max Visible Distance: 8455 m")
        self.coords_label = QLabel("Coords: (2030, 1925)")

        layout.addWidget(self.visible_label)
        layout.addSpacing(20)
        layout.addWidget(self.blocked_label)
        layout.addSpacing(20)
        layout.addWidget(self.distance_label)
        layout.addSpacing(20)
        layout.addWidget(self.coords_label)
        layout.addStretch()