import math

import arcade
import numpy as np

EPSILON: float = 10 ** -12


def normalize(v: arcade.Vector) -> arcade.Vector:
    """Gets vector and returns a new normalized copy.

    :param v: given vector
    :type v: arcade.Vector
    :return: normalized copy of vector v
    :rtype: arcade.Vector
    """
    mag: float = np.sqrt(v[0]*v[0] + v[1]*v[1])
    if mag <= EPSILON:  return v
    else:               return (v[0]/mag, v[1]/mag)


def magnitude(v: arcade.Vector) -> float:
    """Gets vector and returns its magnitude/length.

    :param v: given vector
    :type v: arcade.Vector
    :return: magnitude/length of that vector
    :rtype: float
    """
    return np.sqrt(v[0]*v[0] + v[1]*v[1])


def clamp(v: arcade.Vector, min: float, max: float) -> arcade.Vector: # TODO check if it works correctly
    """Gets vector and returns new clamped copy of it.

    :param v: given vector
    :type v: arcade.Vector
    :param min: minimum length of vector v
    :type min: float
    :param max: maximum length of vector v
    :type max: float
    :return: clamped copy of vector v
    :rtype: arcade.Vector
    """
    mag: float = np.sqrt(v[0]*v[0] + v[1]*v[1])
    if (min <= mag <= max) or mag <= EPSILON: return v
    if mag < min:
        ratio: float = min / mag
        return (v[0] * ratio, v[1] * ratio)
    else:
        ratio: float = max / mag
        return (v[0] * ratio, v[1] * ratio)


def map_range(value: float, from_min: float, from_max: float, to_min: float, to_max: float) -> float:
    return (value - from_min) * (to_max - to_min) / (from_max - from_min) + to_min


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


def distance2D(vec1: arcade.Vector, vec2: arcade.Vector) -> float:
    return math.sqrt((vec1[0] - vec2[0]) ** 2 + (vec1[1] - vec2[1]) ** 2)


if __name__ == '__main__':
    pass
