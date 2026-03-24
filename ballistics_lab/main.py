from __future__ import annotations

from ballistics_lab.cli import parse_inputs
from ballistics_lab.plotting import plot_trajectory, plot_state_timeseries
from ballistics_lab.solvers.ballistic_vacuum import VacuumBallisticSolver


def main() -> None:
    args, launch, env, t = parse_inputs()

    solver = VacuumBallisticSolver()
    traj = solver.solve(launch, env, t).clipped()

    print(f"Launch angle: {launch.angle_deg:.3f} deg")
    print(f"Flight time:   {traj.t[-1]:.3f} s")
    print(f"Range:         {traj.x[-1]:.3f} m")
    print(f"Impact y:      {traj.y[-1]:.3f} m")

    plot_trajectory(traj)

    if args.plot_velocity:
        plot_state_timeseries(traj)


if __name__ == "__main__":
    main()
