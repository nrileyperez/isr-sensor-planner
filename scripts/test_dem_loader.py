from pathlib import Path

from app.terrain.dem_loader import load_dem


def main():
    dem_path = Path("data/sample/san_diego_dem.tif")
    dem = load_dem(dem_path)

    print("DEM loaded successfully")
    print(f"Shape: {dem.elevation.shape}")
    print(f"Bounds: {dem.bounds}")
    print(f"Resolution: {dem.resolution}")
    print(f"CRS: {dem.crs}")
    print(f"Min elevation: {dem.elevation[np.isfinite(dem.elevation)].min()}")
    print(f"Max elevation: {dem.elevation[np.isfinite(dem.elevation)].max()}")


if __name__ == "__main__":
    import numpy as np
    main()