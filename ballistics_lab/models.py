from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class LaunchState:
    x0: float
    y0: float
    speed: float
    angle_deg: float


@dataclass(frozen=True)
class Environment:
    gravity: float = 9.81


@dataclass(frozen=True)
class Target:
    x: float
    y: float


@dataclass(frozen=True)
class Trajectory:
    t: np.ndarray
    x: np.ndarray
    y: np.ndarray
    vx: np.ndarray
    vy: np.ndarray

    @property
    def apex(self) -> float:
        return float(np.max(self.y))

    @property
    def has_impact(self) -> bool:
        return bool(np.any(self.y < 0.0))

    @property
    def impact_index(self) -> int:
        below = np.where(self.y < 0.0)[0]
        if len(below) == 0:
            return len(self.y) - 1
        return int(below[0])

    def clipped(self) -> "Trajectory":
        idx = self.impact_index + 1
        return Trajectory(
            t=self.t[:idx],
            x=self.x[:idx],
            y=self.y[:idx],
            vx=self.vx[:idx],
            vy=self.vy[:idx],
        )
