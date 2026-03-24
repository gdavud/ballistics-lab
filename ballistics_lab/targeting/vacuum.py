from __future__ import annotations

import math
from dataclasses import dataclass

from ballistics_lab.models import Target, Environment


@dataclass(frozen=True)
class FiringSolution:
    angle_low_deg: float
    angle_high_deg: float


def solve_firing_angles_for_speed(
    speed: float,
    target: Target,
    env: Environment,
    x0: float = 0.0,
    y0: float = 0.0,
) -> FiringSolution:
    """
    Solve launch angles for a fixed speed in vacuum.

    Uses:
        y = x tan(theta) - g x^2 / (2 v^2 cos^2(theta))

    Converted into quadratic in tan(theta).
    """
    dx = target.x - x0
    dy = target.y - y0
    g = env.gravity
    v = speed

    if dx <= 0:
        raise ValueError("Target must be in front of launcher (dx > 0).")

    disc = v**4 - g * (g * dx**2 + 2 * dy * v**2)
    if disc < 0:
        raise ValueError("Target is unreachable for the given speed.")

    root = math.sqrt(disc)

    tan_low = (v**2 - root) / (g * dx)
    tan_high = (v**2 + root) / (g * dx)

    angle_low = math.degrees(math.atan(tan_low))
    angle_high = math.degrees(math.atan(tan_high))

    return FiringSolution(
        angle_low_deg=angle_low,
        angle_high_deg=angle_high,
    )
