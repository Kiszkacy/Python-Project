
import arcade
import numpy as np

# creates new normalized vector
def normalize(v: arcade.Vector) -> arcade.Vector:
    mag: float = np.sqrt(v[0]*v[0] + v[1]*v[1])
    if mag <= 0.0:  return v
    else:           return (v[0]/mag, v[1]/mag)


def length(v: arcade.Vector) -> float:
    return np.sqrt(v[0]*v[0] + v[1]*v[1])


if __name__ == '__main__':
    pass
