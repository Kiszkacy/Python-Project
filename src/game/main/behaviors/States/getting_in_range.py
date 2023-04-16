import math

import arcade
import numpy as np

from src.game.main.behaviors.state import State
from src.game.main.enums.behavior_status import BehaviorStatus
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.interfaces.collidable import Collidable
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.util.math import distance2D


class GettingInRange(State):
    """
    context here, is a form of `tuple(target: Sprite, range: int|float)` that we have to reach, after getting in range of
    target it return's its parent as next state.\n
    """

    def __init__(self, body: arcade.Sprite | Collidable, parent: State, context: tuple[arcade.Sprite, int | float], interruptable=False):
        super().__init__(body, interruptable=interruptable, context=context)
        self.parent = parent
        self.path = None
        self.target: arcade.Sprite = context[0]
        self.range: int | float = context[1]
        self.barrier_list = None
        self.time_since_check = 0
        self.progress = 0


    def execute(self, delta_time: float = 1 / 60):
        recheck_time: float = 2  # how often should we check targets position
        self.time_since_check += delta_time

        if self.status == BehaviorStatus.IDLE or self.status == BehaviorStatus.INTERRUPTED:
            self.status = BehaviorStatus.RUNNING
            self.barrier_list = EntityHandler.barrier_list
            self.calculate_path()
        elif self.time_since_check > recheck_time:
            self.time_since_check = 0
            # if target moved to far away from our path, we need to calculate it again
            if distance2D(self.path[-1], self.target.position) > self.range:
                self.calculate_path()

        # check if we are close to one of the checkpoints on a path #TODO this number shouldn't be hardcoded?
        if self.path and self.body.collision_radius > distance2D(self.body.position, self.path[self.progress]):
            self.progress += 1

        if (self.path is None  # there is no path to the target
                or len(self.path) <= self.progress  # we reached end of path
                or (distance2D(self.body.position, self.target.position) < self.range
                    and arcade.has_line_of_sight(self.body.position,
                                                 self.target.position,
                                                 EntityHandler.categorized[ObjectCategory.STATIC], self.range))):  # we reached our target
            self.status = BehaviorStatus.NEXT_STATE
            return

        x_diff: float = self.path[self.progress][0] - self.body.position[0]
        y_diff: float = self.path[self.progress][1] - self.body.position[1]
        target_angle_rad: float = np.arctan2(y_diff, x_diff)
        if target_angle_rad < 0:
            target_angle_rad += 2*math.pi
        self.body.rotate_towards(delta_time, target_angle_rad)
        if abs(target_angle_rad - np.deg2rad(self.body.angle)) < 0.1:
            self.body.fly(delta_time)


    def calculate_path(self):
        self.time_since_check = 0
        self.progress = 0
        self.path = arcade.astar_calculate_path(self.body.position,
                                                self.target.position,
                                                self.barrier_list,
                                                diagonal_movement=True)
        if self.path:
            self.path.pop(0)

    def next(self):
        super(GettingInRange, self).next()
        if self.path is not None:
            self.parent.context = (*self.context, True)
        else:
            self.parent.context = (*self.context, False)
        return self.parent

    def reset(self, context):
        super(GettingInRange, self).reset(context)
        self.target = context[0]
        self.range = context[1]
