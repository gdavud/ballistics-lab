from __future__ import annotations

from ballistics_lab.cli import parse_inputs
from ballistics_lab.plotting import plot_trajectory
from ballistics_lab.solvers.vacuum import VacuumTrajectorySolver


def main() -> None:
    _, launch, env, t = parse_inputs()
    solver = VacuumTrajectorySolver()
    raw_traj = solver.solve(launch, env, t).clipped()
    traj = raw_traj.clipped()

    print(f"Launch angle:  {launch.angle_deg:.3f} deg")
    print(f"Apex:          {traj.apex:.3f} m")

    if raw_traj.has_impact:
        print(f"Flight time:   {traj.t[-1]:.3f} s")
        print(f"Range:         {traj.x[-1]:.3f} m")
        print(f"Impact:        {traj.y[-1]:.3f} m")
    else:
        print("Ground impact not reached within tmax.")
        print(f"Final time:    {traj.t[-1]:.3f} s")
        print(f"Final x:       {traj.x[-1]:.3f} m")
        print(f"Final y:       {traj.y[-1]:.3f} m")

    plot_trajectory(env, traj)


if __name__ == "__main__":
    main()
