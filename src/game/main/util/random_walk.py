import arcade
import random
from collections import deque


class RandomWalk:

    def __init__(self, body: arcade.Sprite, area: tuple[int, int], smoothing_factor=0.2, history_length=10):
        self.body: arcade.Sprite = body
        body.position = [random.randint(0, area[0]), random.randint(0, area[1])]
        body.angle = random.randint(0, 360)
        body.update()
        self.area: tuple[int, int] = area
        self.last_thetas: deque = deque(maxlen=history_length)
        self.last_speeds: deque = deque(maxlen=history_length)
        self.smoothing_factor = smoothing_factor

    def walk(self, delta_time: float):
        speed: float = random.random() - 0.3
        self.last_speeds.append(speed)
        # Exponential smoothing for speed
        speed = self.exponential_smoothing(list(self.last_speeds))

        angle: float = random.random() * 360 - 180
        self.last_thetas.append(angle)
        # Exponential smoothing for angle
        angle = self.exponential_smoothing(list(self.last_thetas))

        self.body.forward(speed * delta_time)
        self.body.turn_left(angle * delta_time)
        # wrapping around the monitor
        self.wrap_position()
        # updating the sprite
        self.body.update()

    def wrap_position(self):
        if self.body.position[0] < 0: self.body.position[0] = self.area[0]
        if self.body.position[1] < 0: self.body.position[1] = self.area[1]
        if self.body.position[0] > self.area[0]: self.body.position[0] = 0
        if self.body.position[1] > self.area[1]: self.body.position[1] = 0

    def exponential_smoothing(self, values):
        smoothed_value = values[-1]
        for value in reversed(values[:-1]):
            smoothed_value = self.smoothing_factor * value + (1 - self.smoothing_factor) * smoothed_value
        return smoothed_value