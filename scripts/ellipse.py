import os
import argparse
import subprocess
import numpy as np
from typing import Any
import matplotlib.pyplot as plt


def plot_ellipse_rasterization(r_x: int,
                               r_y: int,
                               center: tuple[int, int],
                               x_step: float,
                               x_inches: int,
                               y_inches: int,
                               DPI: int) -> None:

    x: np.ndarray[tuple[int], np.dtype[Any]] = np.arange(-r_x, r_x + x_step, x_step) + center[0]
    y_p: np.ndarray[tuple[int], np.dtype[Any]] =  (r_y/r_x)*np.sqrt(np.square(r_x) - np.square(x - center[0])) + center[1]
    y_n: np.ndarray[tuple[int], np.dtype[Any]] = -(r_y/r_x)*np.sqrt(np.square(r_x) - np.square(x - center[0])) + center[1]

    fig, ax = plt.subplots()
    fig.set_size_inches(x_inches, y_inches)
    fig.set_dpi(DPI)

    ax.plot(x, y_p)
    ax.plot(x, y_n)

    ax.set_xticks(np.arange(-r_x - 2 + center[0], r_x + 3 + center[0], 1))
    ax.set_yticks(np.arange(-r_y - 2 + center[1], r_y + 3 + center[1], 1))
    ax.set_xlabel("X")
    ax.set_ylabel("Y", rotation=0)
    ax.set_xlim((-r_x - 2 + center[0], r_x + 2 + center[0]))
    ax.set_ylim((-r_y - 2 + center[1], r_y + 2 + center[1]))
    ax.set_title("Ellipse")
    ax.set_aspect("equal")
    ax.grid()

    ax.axhline(center[1])
    ax.axvline(center[0])

    fig.tight_layout()

    fig.savefig("ellipse.png")
    subprocess.run(["feh", "ellipse.png"])
    os.remove("ellipse.png")


if (__name__=="__main__"):

    parser = \
       argparse.ArgumentParser(prog="EllipseRasterization",
                               description="Visualization of Ellipse Rasterization Algorithm") 

    parser.add_argument("X_axis_radius", type=int)
    parser.add_argument("Y_axis_radius", type=int)
    parser.add_argument("X_center", type=int)
    parser.add_argument("Y_center", type=int)
    parser.add_argument("x_step", type=float)
    parser.add_argument("X_inches", type=int)
    parser.add_argument("Y_inches", type=int)
    parser.add_argument("DPI", type=int)
    args: argparse.Namespace = parser.parse_args()

    plot_ellipse_rasterization(args.X_axis_radius,
                               args.Y_axis_radius,
                               (args.X_center,
                                args.Y_center),
                               args.x_step,
                               args.X_inches,
                               args.Y_inches,
                               args.DPI)
