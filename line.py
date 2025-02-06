import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from typing import Any
import argparse
import subprocess
import os


matplotlib.use("Agg")
plt.rcParams['text.usetex'] = True


def line(x_1: int, y_1: int,
         x_2: int, y_2: int) -> np.ndarray[tuple[int, int], np.dtype[Any]]:

    delta_x: int = x_2 - x_1
    delta_y: int = y_2 - y_1

    sgn_delta_x: int = np.sign(delta_x)
    sgn_delta_y: int = np.sign(delta_y)

    non_steep: bool = abs(delta_x) > abs(delta_y)

    N: int = abs(delta_x if non_steep else delta_y)
    T: int = N - 2*(sgn_delta_y*((N - 1)*y_1 + y_2) if non_steep else sgn_delta_x*((N - 1)*x_1 + x_2))

    points: np.ndarray[tuple[int, int], np.dtype[Any]] = np.empty((N + 1, 2), dtype=int)
    points[0] = (x_1, y_1)
    points[N] = (x_2, y_2)

    decision: bool

    for n in range(0, N - 1):

        decision = 2*(sgn_delta_y*(n*delta_y - N*points[n][1]) if non_steep else sgn_delta_x*(n*delta_x - N*points[n][0])) >= T  # noqa: E501

        points[n + 1] = \
            (points[n][0] + (sgn_delta_x if non_steep else (sgn_delta_x if decision else 0)),
             points[n][1] + ((sgn_delta_y if decision else 0) if non_steep else sgn_delta_y))

    return points


def plot_line_rasterization(x_1: int, y_1: int,
                            x_2: int, y_2: int) -> None:

    x_min: int = min(x_1, x_2) - 2
    x_max: int = max(x_1, x_2) + 2
    y_min: int = min(y_1, y_2) - 2
    y_max: int = max(y_1, y_2) + 2

    abs_delta_x: int = abs(x_2 - x_1)
    abs_delta_y: int = abs(y_2 - y_1)

    fig, ax = plt.subplots()
    if (abs_delta_x > abs_delta_y):
        fig.set_size_inches(0.6*abs_delta_x, abs_delta_y)
    else:
        fig.set_size_inches(abs_delta_x, 0.6*abs_delta_y)
    fig.set_dpi(100)

    ax.plot([x_1, x_2], [y_1, y_2], color="blue")
    ax.plot(x_1, y_1, marker="o", color="black")
    ax.plot(x_2, y_2, marker="o", color="black")

    points: np.ndarray[tuple[int, int], np.dtype[Any]] = line(x_1, y_1, x_2, y_2)
    print(points)
    for i in range(0, len(points) - 1):
        ax.plot([points[i][0], points[i + 1][0]],
                [points[i][1], points[i + 1][1]],
                marker="x", color="black")

    ax.set_xticks(np.arange(x_min, x_max + 1, 1))
    ax.set_yticks(np.arange(y_min, y_max + 1, 1))
    ax.set_xlabel("X")
    ax.set_ylabel("Y", rotation=0)
    ax.set_xlim((x_min, x_max))
    ax.set_ylim((y_min, y_max))
    ax.set_title("Line")
    ax.set_aspect("equal")
    ax.grid()

    fig.savefig("line.png")
    subprocess.run(["feh", "line.png"])
    os.remove("line.png")


if (__name__ == "__main__"):

    parser = \
        argparse.ArgumentParser(prog="LineRasterization",
                                description="Visualization of Line Rasterization Algorithm")

    parser.add_argument("X_1", type=int)
    parser.add_argument("Y_1", type=int)
    parser.add_argument("X_2", type=int)
    parser.add_argument("Y_2", type=int)
    args = parser.parse_args()

    plot_line_rasterization(args.X_1, args.Y_1,
                            args.X_2, args.Y_2)
