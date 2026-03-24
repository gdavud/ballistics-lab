from __future__ import annotations

import math
import numpy as np

from ballistics_lab.models import LaunchState, Environment, Trajectory
from ballistics_lab.solvers.base import TrajectorySolver


class VacuumTrajectorySolver(TrajectorySolver):
    def solve(
        self,
        launch: LaunchState,
        env: Environment,
        t: np.ndarray,
    ) -> Trajectory:
        theta = math.radians(launch.angle_deg)
        vx0 = launch.speed * math.cos(theta)
        vy0 = launch.speed * math.sin(theta)
        g = env.gravity

        x = launch.x0 + vx0 * t
        y = launch.y0 + vy0 * t - 0.5 * g * t**2
        vx = np.full_like(t, vx0, dtype=float)
        vy = vy0 - g * t

        return Trajectory(t=t, x=x, y=y, vx=vx, vy=vy)
