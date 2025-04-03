import subprocess
import numpy as np
import matplotlib.pyplot as plt
import os
import argparse
from typing import Any


def py_impl_circle(radius: int,
                   center: tuple[int, int]) -> np.ndarray[tuple[int, int], np.dtype[Any]]:

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

    overflow: int = 1 if first_octant_points[N - 1][0] == first_octant_points[N - 1][1] else 0
    M: int = N - overflow
    Q: int = 2*N - 1 - overflow

    points: np.ndarray[tuple[int, int], np.dtype[Any]] = np.empty((4*Q, 2), dtype=int)

    # Right-most point
    points[0] = \
        (first_octant_points[0][0] + center[0],
         first_octant_points[0][1] + center[1])

    # Upper-most point
    points[Q] = \
        (first_octant_points[0][1] + center[0],
         first_octant_points[0][0] + center[1])

    # Left-most point
    points[2*Q] = \
        (-first_octant_points[0][0] + center[0],
          first_octant_points[0][1] + center[1])

    # Bottom-most point
    points[3*Q] = \
        (-first_octant_points[0][1] + center[0],
         -first_octant_points[0][0] + center[1])

    if overflow:

        # Upper-left diagonal point
        points[N - 1] = \
            (first_octant_points[N - 1][0] + center[0],
             first_octant_points[N - 1][1] + center[1])

        # Upper-right diagonal point
        points[2*Q - (N - 1)] = \
            (-first_octant_points[N - 1][0] + center[0],
              first_octant_points[N - 1][1] + center[1])

        # Lower-right diagonal point
        points[2*Q + (N - 1)] = \
            (-first_octant_points[N - 1][0] + center[0],
             -first_octant_points[N - 1][1] + center[1])

        # Lower-left diagonal point
        points[4*Q - (N - 1)] = \
            ( first_octant_points[N - 1][0] + center[0],
             -first_octant_points[N - 1][1] + center[1])


    for m in range(1, M):

        # First Octant
        points[m] = \
            (first_octant_points[m][0] + center[0],
             first_octant_points[m][1] + center[1])

        # Second Octant
        points[Q - m] = \
            (first_octant_points[m][1] + center[0],
             first_octant_points[m][0] + center[1])

        # Third Octant
        points[Q + m] = \
            (-first_octant_points[m][1] + center[0],
              first_octant_points[m][0] + center[1])
        # Fourth Octant
        points[2*Q - m] = \
            (-first_octant_points[m][0] + center[0],
              first_octant_points[m][1] + center[1])

        # Fifth Octant
        points[2*Q + m] = \
            (-first_octant_points[m][0] + center[0],
             -first_octant_points[m][1] + center[1])

        # Sixth Octant
        points[3*Q - m] = \
            (-first_octant_points[m][1] + center[0],
             -first_octant_points[m][0] + center[1])

        # Seventh Octant
        points[3*Q + m] = \
            ( first_octant_points[m][1] + center[0],
             -first_octant_points[m][0] + center[1])

        # Eighth Octant
        points[4*Q - m] = \
            ( first_octant_points[m][0] + center[0],
             -first_octant_points[m][1] + center[1])

    return points


def plot_circle_rasterization(radius: int,
                              center: tuple[int, int],
                              x_step: float,
                              x_inches: int,
                              y_inches: int,
                              dpi: int) -> None:

    x: np.ndarray[tuple[int], np.dtype[Any]] = np.arange(-radius, radius + x_step, x_step) + center[0]
    top_half: np.ndarray[tuple[int], np.dtype[Any]] = np.sqrt(radius**2 - (x - center[0])**2) + center[1]
    bottom_half: np.ndarray[tuple[int], np.dtype[Any]] = -np.sqrt(radius**2 - (x - center[0])**2) + center[1]

    fig, ax = plt.subplots()
    fig.set_size_inches(x_inches, y_inches)
    fig.set_dpi(dpi)

    ax.plot(x,    top_half)
    ax.plot(x, bottom_half)

    points: np.ndarray[tuple[int, int], np.dtype[Any]] = py_impl_circle(radius, center)
 
    for i in range(0, len(points)):
        print("({X: 2d}, {Y: 2d}), {angle:.2f}".format(X=points[i][0],
                                                       Y=points[i][1],
                                                       angle=(180/np.pi)*np.arctan2(points[i][1] - center[1],
                                                                                    points[i][0] - center[0])))

    for i in range(0, len(points) - 1):
        ax.plot([points[i][0], points[i + 1][0]],
                [points[i][1], points[i + 1][1]],
                marker="x", color="black")

    ax.set_xticks(np.arange(-radius - 2 + center[0], radius + 3 + center[0], 1))
    ax.set_yticks(np.arange(-radius - 2 + center[1], radius + 3 + center[1], 1))
    ax.set_xlabel("X")
    ax.set_ylabel("Y", rotation=0)
    ax.set_xlim((-radius - 2 + center[0], radius + 2 + center[0]))
    ax.set_ylim((-radius - 2 + center[1], radius + 2 + center[1]))
    ax.set_title("Circle")
    ax.set_aspect("equal")
    ax.grid()

    ax.axhline(center[1])
    ax.axvline(center[0])

    fig.tight_layout()

    fig.savefig("circle.png")
    subprocess.run(["feh", "circle.png"])
    os.remove("circle.png")




if (__name__ == "__main__"):

    parser = \
        argparse.ArgumentParser(prog="CircleRasterization",
                                description="Visualization of Circle Rasterization Algorithm")

    parser.add_argument("radius", type=int)
    parser.add_argument("X_center", type=int)
    parser.add_argument("Y_center", type=int)
    parser.add_argument("x_step", type=float)
    parser.add_argument("X_inches", type=int)
    parser.add_argument("Y_inches", type=int)
    parser.add_argument("DPI", type=int)
    args: argparse.Namespace = parser.parse_args()

    plot_circle_rasterization(args.radius,
                              (args.X_center,
                               args.Y_center),
                              args.x_step,
                              args.X_inches,
                              args.Y_inches,
                              args.DPI)
