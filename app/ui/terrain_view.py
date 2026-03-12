from pathlib import Path

import pyvista as pv
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from pyvistaqt import QtInteractor

import numpy as np

from app.terrain.dem_loader import load_dem
from app.terrain.mesh_builder import build_structured_grid


class TerrainView(QFrame):
    def __init__(self):
        super().__init__()

        self.setFrameShape(QFrame.StyledPanel)

        self.scenario = None
        self.dem = None
        self.grid = None
        self.sensor_actor = None

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.title_label = QLabel("3D Terrain Scene")
        layout.addWidget(self.title_label)

        self.plotter = QtInteractor(self)
        layout.addWidget(self.plotter.interactor)

        # Delay first render until Qt event loop is active
        QTimer.singleShot(300, self._initialize_scene)

    def set_scenario(self, scenario):
        """Store scenario state for later sensor phases."""
        self.scenario = scenario

    def _initialize_scene(self):
        dem_path = Path("data/sample/san_diego_dem.tif")
        self.title_label.setText("3D Terrain Scene — loading terrain...")

        if not dem_path.exists():
            self.title_label.setText(f"3D Terrain Scene — DEM not found: {dem_path}")
            self._show_fallback_sphere()
            return

        try:
            dem = load_dem(dem_path)
            self.dem = dem

            # Conservative embedded rendering settings
            grid = build_structured_grid(
                dem,
                downsample_step=16,
                z_scale=8.0,
            )
            self.grid = grid

            self.plotter.clear()
            self.plotter.set_background("black")
            self.plotter.add_mesh(
                grid,
                scalars="elevation",
                cmap="terrain",
                show_edges=False,
                smooth_shading=False,
                lighting=False,
            )
            self.plotter.add_axes()
            self.plotter.reset_camera()
            self.plotter.render()

            self.title_label.setText(
                f"3D Terrain Scene — {dem_path.name} "
                f"(downsample=16, points={grid.n_points:,})"
            )

            # Draw initial sensor marker once terrain is ready
            if self.scenario is not None:
                self.update_sensor_marker()

        except Exception as exc:
            self.title_label.setText(f"3D Terrain Scene — render error: {exc}")
            self._show_fallback_sphere()

    def _show_fallback_sphere(self):
        """Fallback so the center panel never stays blank."""
        self.plotter.clear()
        self.plotter.set_background("black")
        sphere = pv.Sphere(radius=1.0, theta_resolution=32, phi_resolution=32)
        self.plotter.add_mesh(sphere, color="lightblue", smooth_shading=True)
        self.plotter.add_axes()
        self.plotter.reset_camera()
        self.plotter.render()

    def _sample_terrain_height(self, x, y):
        if self.dem is None:
            return 0.0

        #terrain mesh is currently built in local raster-space coordinates
        elevation = self.dem.elevation
        rows, cols = elevation.shape

        #retrive spatial size from DEM
        x_res = self.dem.resolution[0]
        y_res = self.dem.resolution[1]

        #convert col and row index  
        col = int(x / x_res)
        row = int(y / y_res)

        #clamping step for valid index to pass
        col = max(0, min(cols - 1, col))
        row = max(0, min(rows - 1, row))

        value = elevation[row, col]

        if np.isnan(value):
            valid = elevation[np.isfinite(elevation)]
            if valid.size == 0:
                return 0.0
            return float(valid.min())

        return float(value)
    
    #place actual sennor marker
    def update_sensor_marker(self):
        if self.scenario is None or self.dem is None:
            return

        x = self.scenario.sensor_x
        y = self.scenario.sensor_y

        terrain_z = self._sample_terrain_height(x, y)
        z = terrain_z + self.scenario.sensor_height

        sensor_geom = pv.Sphere(
            radius=100,
            center=(x, y, z),
            theta_resolution=24,
            phi_resolution=24,
        )

        if self.sensor_actor is not None:
            self.plotter.remove_actor(self.sensor_actor)

        self.sensor_actor = self.plotter.add_mesh(
            sensor_geom,
            color="red",
            smooth_shading=True,
        )

        self.plotter.render()