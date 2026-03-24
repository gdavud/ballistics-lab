from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="artillery-sim",
        description="2D point-mass artillery simulator (vacuum ballistic model).",
    )

    parser.add_argument("--x0", type=float, default=0.0, help="Initial x position [m]")
    parser.add_argument("--y0", type=float, default=0.0, help="Initial y position [m]")
    parser.add_argument("--speed", type=float, required=True, help="Launch speed [m/s]")
    parser.add_argument("--angle", type=float, help="Launch angle [deg]")
    parser.add_argument("--gravity", type=float, default=9.81, help="Gravity [m/s^2]")

    parser.add_argument("--target-x", type=float, help="Target x position [m]")
    parser.add_argument("--target-y", type=float, default=0.0, help="Target y position [m]")
    parser.add_argument(
        "--arc",
        choices=("low", "high"),
        default="low",
        help="Choose low or high firing solution when targeting is used",
    )

    parser.add_argument(
        "--tmax",
        type=float,
        default=120.0,
        help="Max simulation time [s]",
    )
    parser.add_argument(
        "--dt",
        type=float,
        default=0.001,
        help="Time step [s]",
    )

    return parser
