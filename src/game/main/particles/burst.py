from dataclasses import dataclass

import arcade.gl

from src.game.main.enums.particle import Particle


@dataclass
class Burst:
    buffer: arcade.gl.Buffer
    vao: arcade.gl.Geometry
    start: float
    particle_type: Particle


if __name__ == '__main__':
    pass
