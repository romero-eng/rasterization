import subprocess
import numpy as np
import matplotlib.pyplot as plt
import os
import argparse
from typing import Any


def py_impl_circle(radius: int) -> np.ndarray[tuple[int, int], np.dtype[Any]]:

    N: int = int(np.floor(radius/np.sqrt(2))) + 1
    tau: int = 4*np.square(radius) - 5

    first_octant_points: np.ndarray[tuple[int, int], np.dtype[Any]] = np.empty((N, 2), dtype=int)
    first_octant_points[0] = (radius, 0)

    decrement: bool

    for n in range(0, N - 1):

        decrement = 4*(np.square(first_octant_points[n][0]) - first_octant_points[n][0] + np.square(n) + 2*n) >= tau

        first_octant_points[n + 1] = \
            (first_octant_points[n][0] - (1 if decrement else 0),
             first_octant_points[n][1] + 1)

    M: int = N - (1 if first_octant_points[N - 1][0] == first_octant_points[N - 1][1] else 0)
    Q: int = N + M
    T: int = 2*Q - 1
    C: int = 2*(T - 1)

    circular_arc_points: np.ndarray[tuple[int, int], np.dtype[Any]] = np.empty((C, 2), dtype=int)

    for n in range(0, N):
        circular_arc_points[n] = first_octant_points[n]

    for m in range(N, Q):
        circular_arc_points[m] = \
            (first_octant_points[M - 1 - m][1],
             first_octant_points[M - 1 - m][0])

    for q in range(Q, T):
        circular_arc_points[q] = \
            (-circular_arc_points[T - 1 - q][0],
              circular_arc_points[T - 1 - q][1])  # noqa: E127

    for t in range(T, C):
        circular_arc_points[t] = \
            ( circular_arc_points[C - t][0],  # noqa: E201
             -circular_arc_points[C - t][1])  # noqa: E128

    return circular_arc_points


def plot_circle_rasterization(radius: int,
                              x_step: float,
                              x_inches: int,
                              y_inches: int,
                              dpi: int) -> None:

    x: np.ndarray[tuple[int], np.dtype[Any]] = np.arange(-radius, radius + x_step, x_step)
    top_half: np.ndarray[tuple[int], np.dtype[Any]] = np.sqrt(radius**2 - x**2)
    bottom_half: np.ndarray[tuple[int], np.dtype[Any]] = -top_half

    fig, ax = plt.subplots()
    fig.set_size_inches(x_inches, y_inches)
    fig.set_dpi(dpi)

    ax.plot(x,    top_half)
    ax.plot(x, bottom_half)

    points: np.ndarray[tuple[int, int], np.dtype[Any]] = py_impl_circle(radius)

    for i in range(0, len(points)):
        print("({X: 2d}, {Y: 2d}), {angle:.2f}".format(X=points[i][0],
                                                       Y=points[i][1],
                                                       angle=(180/np.pi)*np.arctan2(points[i][1],
                                                                                    points[i][0])))

    for i in range(0, len(points) - 1):
        ax.plot([points[i][0], points[i + 1][0]],
                [points[i][1], points[i + 1][1]],
                marker="x", color="black")

    ax.set_xticks(np.arange(-radius - 2, radius + 3, 1))
    ax.set_yticks(np.arange(-radius - 2, radius + 3, 1))
    ax.set_xlabel("X")
    ax.set_ylabel("Y", rotation=0)
    ax.set_xlim((-radius - 2, radius + 2))
    ax.set_ylim((-radius - 2, radius + 2))
    ax.set_title("Circle")
    ax.set_aspect("equal")
    ax.grid()

    fig.tight_layout()

    fig.savefig("circle.png")
    subprocess.run(["feh", "circle.png"])
    os.remove("circle.png")


if (__name__ == "__main__"):

    parser = \
        argparse.ArgumentParser(prog="CircleRasterization",
                                description="Visualization of Circle Rasterization Algorithm")

    parser.add_argument("radius", type=int)
    parser.add_argument("x_step", type=float)
    parser.add_argument("X_inches", type=int)
    parser.add_argument("Y_inches", type=int)
    parser.add_argument("DPI", type=int)
    args: argparse.Namespace = parser.parse_args()

    plot_circle_rasterization(args.radius,
                              args.x_step,
                              args.X_inches,
                              args.Y_inches,
                              args.DPI)
