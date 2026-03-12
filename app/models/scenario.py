from dataclasses import dataclass

@dataclass
class Scenario:
    terrain_file_path: str = "data/sample/san_diego_dem.tif"

    sensor_x: float = 2000.0
    sensor_y: float = 2000.0
    sensor_height: float = 300.0

    azimuth: float = 90.0
    tilt: float = 0.0
    field_of_view: float = 60.0
    max_range: float = 5000.0

    show_terrain: bool = True
    show_sensor: bool = True
    show_los: bool = False
    show_visible_area: bool = False
    show_occlusion_mask: bool = False