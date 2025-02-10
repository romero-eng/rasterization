from . import Rasterization


def Line(x_1: int, y_1: int, x_2: int, y_2: int) -> list[tuple[int, int]]:
    return Rasterization.Line(x_1, y_1, x_2, y_2)


