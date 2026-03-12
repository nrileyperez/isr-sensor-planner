from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import rasterio


@dataclass
class DEMData:
    elevation: np.ndarray
    bounds: tuple[float, float, float, float]
    transform: object
    crs: object
    resolution: tuple[float, float]
    width: int
    height: int
    nodata: float | None


def load_dem(path: str | Path) -> DEMData:
    """
    Load a DEM GeoTIFF and return elevation data plus key metadata.
    """
    path = Path(path)

    with rasterio.open(path) as src:
        elevation = src.read(1).astype(np.float32)

        nodata = src.nodata
        if nodata is not None:
            elevation = np.where(elevation == nodata, np.nan, elevation)

        bounds = (src.bounds.left, src.bounds.bottom, src.bounds.right, src.bounds.top)
        transform = src.transform
        crs = src.crs
        resolution = src.res
        width = src.width
        height = src.height

    return DEMData(
        elevation=elevation,
        bounds=bounds,
        transform=transform,
        crs=crs,
        resolution=resolution,
        width=width,
        height=height,
        nodata=nodata,
    )