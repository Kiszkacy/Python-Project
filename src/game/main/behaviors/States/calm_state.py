import numpy as np

from src.game.main.behaviors.state import State
from src.game.main.entities.ship import Ship


class CalmState(State):

    def __init__(self, body: Ship):
        super().__init__(body, interruptable=True)

    def execute(self, delta_time: float = 1 / 60):
        # print("CALM")
        target_angle_rad: float = np.deg2rad(self.body.angle + 3)
        self.body.rotate_towards(delta_time, target_angle_rad)
        self.body.fly(delta_time)
