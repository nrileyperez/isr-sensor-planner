from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel

from pyvistaqt import QtInteractor

from app.terrain.dem_loader import load_dem
from app.terrain.mesh_builder import build_structured_grid


class TerrainView(QFrame):
    def __init__(self):
        super().__init__()

        self.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.title_label = QLabel("3D Terrain Scene")
        layout.addWidget(self.title_label)

        self.plotter = QtInteractor(self)
        layout.addWidget(self.plotter.interactor)

        # Delay first render until the Qt event loop is running
        QTimer.singleShot(200, self._initialize_scene)

    def _initialize_scene(self):
        """Load the DEM from Phase 1 and render it in the embedded view."""
        dem_path = Path("data/sample/san_diego_dem.tif")

        if not dem_path.exists():
            self.title_label.setText(f"3D Terrain Scene — DEM not found: {dem_path}")
            return

        try:
            dem = load_dem(dem_path)

            # Use a conservative embedded rendering setting for stability.
            grid = build_structured_grid(
                dem,
                downsample_step=8,
                z_scale=15.0,
            )

            self.plotter.set_background("black")
            self.plotter.add_mesh(
                grid,
                scalars="elevation",
                cmap="terrain",
                show_edges=False,
                smooth_shading=True,
            )
            self.plotter.add_axes()
            self.plotter.reset_camera()
            self.plotter.render()

            self.title_label.setText(
                f"3D Terrain Scene — {dem_path.name} "
                f"(downsample=8, points={grid.n_points:,})"
            )
        except Exception as exc:
            self.title_label.setText(f"3D Terrain Scene — render error: {exc}")