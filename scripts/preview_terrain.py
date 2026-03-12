from pathlib import Path

import pyvista as pv

from app.terrain.dem_loader import load_dem
from app.terrain.mesh_builder import build_structured_grid


DOWNSAMPLE_STEP = 2
Z_SCALE = 50.0
# NOTE:
# Full-resolution rendering (downsample_step=1) causes instability/segfaults
# on the current local Mac + PyVista/VTK setup for this DEM size (san_dieg_dem.tif)
# Use step=2 as the safe default for development.

def main():
    dem_path = Path("data/sample/san_diego_dem.tif")

    dem = load_dem(dem_path)
    grid = build_structured_grid(dem, DOWNSAMPLE_STEP, Z_SCALE)

    plotter = pv.Plotter()
    plotter.add_mesh(
        grid,
        scalars="elevation",
        cmap="terrain",
        show_edges=False,
        lighting=False,
    )
    plotter.add_axes()
    plotter.show_grid()
    plotter.show()


if __name__ == "__main__":
    main()