import arcade
import numpy as np

EPSILON = 10 ** -12


def det(x, y, z) -> float | int:
    return (y[0] - x[0]) * (z[1] - x[1]) - (y[1] - x[1]) * (z[0] - x[0])


def sign_of_det(x, y, z) -> float | int:
    det_val = det(x, y, z)
    if det_val > EPSILON:
        return 1
    elif det_val < -EPSILON:
        return -1
    return 0


def intersects_lines(line1, line2) -> np.ndarray | None:
    # Check if the line segments intersect
    if sign_of_det(*line1, line2[0]) != sign_of_det(*line1, line2[1]) and sign_of_det(*line2, line1[0]) != sign_of_det(
            *line2, line1[1]):
        # Calculate the intersection point
        x1, y1, x2, y2 = line1[0][0], line1[0][1], line1[1][0], line1[1][1]
        x3, y3, x4, y4 = line2[0][0], line2[0][1], line2[1][0], line2[1][1]
        intersection_x: float = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / (
                    (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        intersection_y: float = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / (
                    (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        return np.array((intersection_x, intersection_y))
    return None


if __name__ == '__main__':
    pass
