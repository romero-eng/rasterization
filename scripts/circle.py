import subprocess
import numpy as np
import matplotlib.pyplot as plt
import os
import argparse


def py_impl_circle(radius: int) -> None:

    


def plot_circle_rasterization(radius: int,
                              x_step: float) -> None:

    x: np.ndarray[int] = np.arange(-radius, radius + x_step, x_step)
    top_half: np.ndarray[int] = np.sqrt(radius**2 - x**2)
    bottom_half: np.ndarray[int] = -top_half
    
    fig, ax = plt.subplots()

    ax.plot(x, top_half)
    ax.plot(x, bottom_half)

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



if (__name__=="__main__"):

    parser = \
        argparse.ArgumentParser(prog="CircleRasterization",
                                description="Visualization of Circle Rasterization Algorithm")

    parser.add_argument("radius", type=int)
    parser.add_argument("x_step", type=float)
    args: argparse.Namespace = parser.parse_args()

    plot_circle_rasterization(args.radius, args.x_step)

