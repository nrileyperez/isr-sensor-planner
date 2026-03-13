# Put reusable geometry helpers here:
#convert azimuth/tilt to 3D direction vector
# x = cos(tilt) * sin(azimuth)
# y = cos(tilt) * cos(azimuth)
# z = sin(tilt) 

#compute cone parameters u
#generate rays if needed

import math
from typing import Tuple


def degrees_to_radians(deg: float) -> float:
    return math.radians(deg)


def azimuth_tilt_to_direction(azimuth_deg: float, tilt_deg: float) -> Tuple[float, float, float]:
    """
    Convert azimuth + tilt into a 3D unit direction vector.

    Conventions:
    - azimuth = 0 points along +Y
    - azimuth = 90 points along +X
    - tilt = 0 is horizontal
    - tilt > 0 points upward
    - tilt < 0 points downward
    """
    az = degrees_to_radians(azimuth_deg)
    tilt = degrees_to_radians(tilt_deg)

    x = math.sin(az) * math.cos(tilt)
    y = math.cos(az) * math.cos(tilt)
    z = math.sin(tilt)

    length = math.sqrt(x * x + y * y + z * z)
    if length == 0:
        return (0.0, 1.0, 0.0)

    return (x / length, y / length, z / length)


def cone_radius_from_fov_and_range(field_of_view_deg: float, max_range: float) -> float:
    """
    Compute cone base radius from full FOV angle and cone length.

    Geometry:
        radius = length * tan(FOV / 2)
    """
    half_angle_rad = math.radians(field_of_view_deg / 2.0)
    return max_range * math.tan(half_angle_rad)


def cone_center_from_origin_and_direction(origin, direction, length: float):
    """
    PyVista's Cone uses a center point, not just an origin.
    So we place the cone center halfway along the direction vector.
    """
    ox, oy, oz = origin
    dx, dy, dz = direction

    return (
        ox + dx * (length / 2.0),
        oy + dy * (length / 2.0),
        oz + dz * (length / 2.0),
    )

