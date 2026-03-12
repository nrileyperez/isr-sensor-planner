from __future__ import annotations

import numpy as np
import pyvista as pv

from app.terrain.dem_loader import DEMData


def downsample_array(array: np.ndarray, step: int) -> np.ndarray:
    """
    Downsample a 2D array by taking every nth row/column.
    """
    if step < 1:
        raise ValueError("step must be >= 1")
    return array[::step, ::step]


def build_structured_grid(dem: DEMData, downsample_step: int = 2, z_scale: float = 15.0) -> pv.StructuredGrid:
    """
    Convert DEM elevation data into a PyVista StructuredGrid.
    """
    elevation = downsample_array(dem.elevation, downsample_step)

    rows, cols = elevation.shape

    x_spacing = dem.resolution[0] * downsample_step
    y_spacing = dem.resolution[1] * downsample_step

    x = np.arange(0, cols * x_spacing, x_spacing, dtype=np.float32)
    y = np.arange(0, rows * y_spacing, y_spacing, dtype=np.float32)

    xx, yy = np.meshgrid(x, y)

    valid_mask = np.isfinite(elevation)
    if not valid_mask.any():
        raise ValueError("Elevation array contains no valid finite values.")

    min_elev = elevation[valid_mask].min()

    zz = np.nan_to_num(elevation, nan=np.nanmin(elevation)) * z_scale

    grid = pv.StructuredGrid(xx, yy, zz)

    grid["elevation"] = zz.ravel(order="F")

    print(f"Downsample step: {downsample_step}")
    print(f"Z-Scale: {z_scale}")
    print(f"Grid points: {grid.n_points}")
    print(f"Grid cells: {grid.n_cells}")

    return grid