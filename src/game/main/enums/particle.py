from enum import IntEnum, auto
from typing import Dict


class Particle(IntEnum):
    DAMAGE      = 0
    COLLISION   = auto()
    PICKUP      = auto()
    DESTROY     = auto()


# pseudo-fake class-dict something
ParticleFragmentShader: Dict[Particle, str] = {
    Particle.DAMAGE:        "default",
    Particle.COLLISION:     "default",
    Particle.PICKUP:        "default",
    Particle.DESTROY:       "default",
}


if __name__ == '__main__':
    pass

