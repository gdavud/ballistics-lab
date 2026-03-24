from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from ballistics_lab.models import Environment, Trajectory


def _speed(traj: Trajectory) -> np.ndarray:
    return np.sqrt(traj.vx**2 + traj.vy**2)


def _acceleration(traj: Trajectory) -> tuple[np.ndarray, np.ndarray]:
    ax = np.gradient(traj.vx, traj.t)
    ay = np.gradient(traj.vy, traj.t)
    return ax, ay


def _energy(
    traj: Trajectory,
    mass: float = 1.0,
    g: float = 9.81,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    speed = _speed(traj)
    kinetic = 0.5 * mass * speed**2
    potential = mass * g * traj.y
    total = kinetic + potential
    return kinetic, potential, total


def _summary_text(
    traj: Trajectory,
    apex_idx: int,
    impact_idx: int,
    g: float = 9.81,
) -> str:
    speed = _speed(traj)

    launch_x = traj.x[0]
    launch_y = traj.y[0]
    impact_x = traj.x[impact_idx]
    impact_y = traj.y[impact_idx]
    range_x = impact_x - launch_x
    flight_time = traj.t[impact_idx]

    apex_x = traj.x[apex_idx]
    apex_y = traj.y[apex_idx]
    apex_t = traj.t[apex_idx]

    launch_speed = speed[0]
    impact_speed = speed[impact_idx]

    launch_angle_deg = np.degrees(np.arctan2(traj.vy[0], traj.vx[0]))

    return "\n".join(
        [
            f"launch pos   : ({launch_x:.3f}, {launch_y:.3f}) m",
            f"launch angle : {launch_angle_deg:.3f} deg",
            f"launch speed : {launch_speed:.3f} m/s",
            f"impact pos   : ({impact_x:.3f}, {impact_y:.3f}) m",
            f"impact speed : {impact_speed:.3f} m/s",
            f"flight time  : {flight_time:.3f} s",
            f"range        : {range_x:.3f} m",
            f"apex         : ({apex_x:.3f}, {apex_y:.3f}) m",
            f"time to apex : {apex_t:.3f} s",
            f"gravity      : {g:.3f} m/s²",
        ]
    )


def plot_results(env: Environment, traj: Trajectory) -> None:
    g = env.gravity

    ax_vals, ay_vals = _acceleration(traj)
    kinetic, potential, total = _energy(traj, g=g)

    apex_idx = int(np.argmax(traj.y))
    impact_idx = len(traj.t) - 1

    fig = plt.figure(figsize=(14, 12))
    gs = fig.add_gridspec(
        3,
        2,
        width_ratios=[1.0, 1.0],
        height_ratios=[2.2, 1.0, 1.0],
    )

    ax_traj = fig.add_subplot(gs[0, 0])
    ax_summary = fig.add_subplot(gs[0, 1])
    ax_pos = fig.add_subplot(gs[1, 0])
    ax_vel = fig.add_subplot(gs[1, 1])
    ax_acc = fig.add_subplot(gs[2, 0])
    ax_energy = fig.add_subplot(gs[2, 1])

    # ----------------------------
    # Trajectory
    # ----------------------------
    ax = ax_traj
    ax.plot(traj.x, traj.y, linewidth=2.5)

    ax.scatter(traj.x[0], traj.y[0], s=50, label="launch")
    ax.scatter(traj.x[apex_idx], traj.y[apex_idx], s=50, label="apex")
    ax.scatter(traj.x[impact_idx], traj.y[impact_idx], s=50, label="impact")
    ax.axhline(0, linewidth=1, alpha=0.5)

    ax.set_title("Trajectory", fontsize=11, loc="left")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.grid(True, alpha=0.3)
    ax.legend()

    x_min, x_max = np.min(traj.x), np.max(traj.x)
    y_min, y_max = np.min(traj.y), np.max(traj.y)

    x_range = x_max - x_min
    y_range = y_max - y_min
    max_range = max(x_range, y_range)

    x_mid = (x_min + x_max) / 2
    y_mid = (y_min + y_max) / 2
    pad = 1.2
    padded_range = max_range * pad

    ax.set_xlim(x_mid - padded_range / 2, x_mid + padded_range / 2)
    ax.set_ylim(y_mid - padded_range / 2, y_mid + padded_range / 2)
    ax.set_aspect("equal", adjustable="box")

    # ----------------------------
    # Summary
    # ----------------------------
    ax = ax_summary
    ax.axis("off")
    ax.set_title("Summary", fontsize=11, loc="left")

    summary = _summary_text(traj, apex_idx, impact_idx, g=g)
    ax.text(
        0,
        0.98,
        summary,
        transform=ax.transAxes,
        va="top",
        ha="left",
        family="monospace",
        fontsize=11,
        bbox=dict(
            boxstyle="round,pad=0.5",
            facecolor="white",
            alpha=0.85,
            edgecolor="0.8",
        ),
    )

    # ----------------------------
    # Position
    # ----------------------------
    ax = ax_pos
    ax.plot(traj.t, traj.x, label="x(t)", linewidth=2)
    ax.plot(traj.t, traj.y, label="y(t)", linewidth=2)
    ax.set_title("Position", fontsize=11, loc="left")
    ax.set_xlabel("t [s]")
    ax.set_ylabel("m")
    ax.grid(True, alpha=0.3)
    ax.legend()

    # ----------------------------
    # Velocity
    # ----------------------------
    ax = ax_vel
    ax.plot(traj.t, traj.vx, label="vx", linewidth=2)
    ax.plot(traj.t, traj.vy, label="vy", linewidth=2)
    ax.plot(traj.t, _speed(traj), label="|v|", linewidth=2, linestyle="--")
    ax.axhline(0, linewidth=1, alpha=0.5)
    ax.set_title("Velocity", fontsize=11, loc="left")
    ax.set_xlabel("t [s]")
    ax.set_ylabel("m/s")
    ax.grid(True, alpha=0.3)
    ax.legend()

    # ----------------------------
    # Acceleration
    # ----------------------------
    ax = ax_acc
    ax.plot(traj.t, ax_vals, label="ax", linewidth=2)
    ax.plot(traj.t, ay_vals, label="ay", linewidth=2)
    ax.axhline(0, linewidth=1, alpha=0.5)
    ax.set_title("Acceleration", fontsize=11, loc="left")
    ax.set_xlabel("t [s]")
    ax.set_ylabel("m/s²")
    ax.grid(True, alpha=0.3)
    ax.legend()

    # ----------------------------
    # Energy
    # ----------------------------
    ax = ax_energy
    ax.plot(traj.t, kinetic, label="KE", linewidth=2)
    ax.plot(traj.t, potential, label="PE", linewidth=2)
    ax.plot(traj.t, total, label="Total", linewidth=2)
    ax.set_title("Energy", fontsize=11, loc="left")
    ax.set_xlabel("t [s]")
    ax.set_ylabel("J (m=1kg)")
    ax.grid(True, alpha=0.3)
    ax.legend()

    fig.tight_layout(pad=2.2)
    plt.show()


def plot_trajectory(env: Environment, traj: Trajectory) -> None:
    plot_results(env, traj)
