import arcade
import numpy as np

from src.game.main.entities.entity import Entity
from src.game.main.movement.movement_type import MovementType
from src.game.main.util.math import normalize


class SinusoidalMovement(MovementType):

    def __init__(self, frequency: float, amplitude: float, speed: float, starting_time: float = 0.0) -> None:
        super(SinusoidalMovement, self).__init__()
        self.frequency: float = frequency
        self.amplitude: float = amplitude
        self.speed: float = speed
        self.time: float = starting_time


    def move(self, delta: float, object: Entity) -> None: # TODO BUG fix moves with slight bias to the right but why?
        self.time += delta
        direction: arcade.Vector = normalize(object.velocity)
        up: arcade.Vector = (-direction[1], direction[0])
        up_speed: float = np.cos(self.time*self.frequency) * self.amplitude
        object.velocity = (up[0]*up_speed + direction[0]*self.speed, up[1]*up_speed + direction[1]*self.speed)
        object.position = (object.position[0] + object.velocity[0]*delta, object.position[1] + object.velocity[1]*delta)



if __name__ == '__main__':
    pass
