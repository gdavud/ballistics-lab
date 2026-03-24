from __future__ import annotations

import numpy as np

from ballistics_lab.config import build_parser
from ballistics_lab.models import LaunchState, Environment, Target
from ballistics_lab.targeting.vacuum import solve_firing_angles_for_speed


def parse_inputs():
    parser = build_parser()
    args = parser.parse_args()

    env = Environment(gravity=args.gravity)

    if args.angle is None and args.target_x is None:
        parser.error("Either --angle or --target-x must be provided.")

    if args.angle is not None and args.target_x is not None:
        parser.error("Use either explicit --angle or targeting (--target-x/--target-y), not both.")

    if args.angle is not None:
        angle_deg = args.angle
    else:
        target = Target(x=args.target_x, y=args.target_y)
        solution = solve_firing_angles_for_speed(
            speed=args.speed,
            target=target,
            env=env,
            x0=args.x0,
            y0=args.y0,
        )
        angle_deg = solution.angle_low_deg if args.arc == "low" else solution.angle_high_deg

    launch = LaunchState(
        x0=args.x0,
        y0=args.y0,
        speed=args.speed,
        angle_deg=angle_deg,
    )

    t = np.arange(0.0, args.tmax + args.dt, args.dt)

    return args, launch, env, t
