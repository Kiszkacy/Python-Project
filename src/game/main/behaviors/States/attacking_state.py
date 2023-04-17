import math
from copy import deepcopy

import numpy as np

from src.game.main.behaviors.state import State
from src.game.main.behaviors.states.getting_in_range import GettingInRange
from src.game.main.entities.ship import Ship
from src.game.main.enums.behavior_status import BehaviorStatus
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.util.math import distance2D


class AttackingState(State):

    def __init__(self, body: Ship, calm: State, context=None):
        super().__init__(body, context)
        self.body: Ship
        self.player = EntityHandler.player
        self.target = self.player if self.context is None else self.context
        self.calm_state = calm
        self.reached_target = False
        self.get_in_range_state = GettingInRange(self.body, self, (self.target, 400))

    def execute(self, delta_time: float = 1 / 60):
        if self.status == BehaviorStatus.IDLE:
            if issubclass(self.context.__class__, Ship):    # it's first time this class is called
                self.status = BehaviorStatus.NEXT_STATE
            elif self.context[2]:   # it's called after calling getting_in_range, and we reached it
                self.status = BehaviorStatus.RUNNING
            else:   # it's called after calling getting_in_range, and we did not reach it
                self.status = BehaviorStatus.IDLE

        else:
            dist = distance2D(self.body.position, self.target.position)
            if dist > 700:
                self.status = BehaviorStatus.IDLE
            elif dist > 400:
                self.status = BehaviorStatus.NEXT_STATE
            else:
                x_diff: float = self.target.position[0] - self.body.position[0]
                y_diff: float = self.target.position[1] - self.body.position[1]
                target_angle_rad: float = np.arctan2(y_diff, x_diff)
                if target_angle_rad < 0:
                    target_angle_rad += 2 * math.pi
                if abs(target_angle_rad - np.deg2rad(self.body.angle)) < 10**-1:
                    self.body.fire()
                else:
                    self.body.rotate_towards(delta_time, target_angle_rad)


    def check(self) -> bool:
        if distance2D(self.body.position, self.player.position) < 700:
            self.target = self.player
            self.context = self.target
            return True
        return False

    def next(self):
        super(AttackingState, self).next()
        self.get_in_range_state.reset((self.target, 400))
        self.reached_target = False
        return self.get_in_range_state


    def __deepcopy__(self, memodict={}):
        cls = self.__class__
        result = cls.__new__(cls)
        memodict[id(self)] = result
        for k, v in self.__dict__.items():
            if k in ["player", "context", "target"]:    # we shouldn't copy this objects
                setattr(result, k, v)
            elif k == "get_in_range_state":
                setattr(result, k, GettingInRange(result.body, result, (result.target, 400)))
            else:
                setattr(result, k, deepcopy(v, memodict))
        return result
    