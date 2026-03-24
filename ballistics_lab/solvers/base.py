from __future__ import annotations

from abc import ABC, abstractmethod
import numpy as np

from ballistics_lab.models import LaunchState, Environment, Trajectory


class TrajectorySolver(ABC):
    @abstractmethod
    def solve(
        self,
        launch: LaunchState,
        env: Environment,
        t: np.ndarray,
    ) -> Trajectory:
        raise NotImplementedError
