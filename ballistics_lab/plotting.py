from __future__ import annotations

import matplotlib.pyplot as plt

from ballistics_lab.models import Trajectory


def plot_trajectory(traj: Trajectory) -> None:
    fig, axes = plt.subplots(3, 1, figsize=(10, 12))

    axes[0].plot(traj.x, traj.y)
    axes[0].set_title("Trajectory")
    axes[0].set_xlabel("x [m]")
    axes[0].set_ylabel("y [m]")
    axes[0].grid(True)

    axes[1].plot(traj.t, traj.x)
    axes[1].set_title("x over time")
    axes[1].set_xlabel("t [s]")
    axes[1].set_ylabel("x [m]")
    axes[1].grid(True)

    axes[2].plot(traj.t, traj.y)
    axes[2].set_title("y over time")
    axes[2].set_xlabel("t [s]")
    axes[2].set_ylabel("y [m]")
    axes[2].grid(True)

    plt.tight_layout()
    plt.show()


def plot_state_timeseries(traj: Trajectory) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))

    axes[0].plot(traj.t, traj.vx, label="vx")
    axes[0].plot(traj.t, traj.vy, label="vy")
    axes[0].set_title("Velocity components over time")
    axes[0].set_xlabel("t [s]")
    axes[0].set_ylabel("velocity [m/s]")
    axes[0].legend()
    axes[0].grid(True)

    speed = (traj.vx**2 + traj.vy**2) ** 0.5
    axes[1].plot(traj.t, speed)
    axes[1].set_title("Speed over time")
    axes[1].set_xlabel("t [s]")
    axes[1].set_ylabel("speed [m/s]")
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()
