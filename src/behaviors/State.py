from src.auxilary.BehaviorStatus import BehaviorStatus
from src.behaviors.behavior import Behavior


class State(Behavior):

    def __init__(self, body, context=None, interruptable=False, resumable=False):
        super().__init__(body)
        self.context = context
        self.interruptable: bool = interruptable
        self.resumable: bool = resumable
        self.status: BehaviorStatus = BehaviorStatus.IDLE  # should be running?


    def execute(self, delta_time: float = 1 / 60):
        pass


    def next(self):
        self.status = BehaviorStatus.IDLE
        return None


    def check(self) -> bool:
        return False


    def reset(self, context):
        self.context = context
        self.status = BehaviorStatus.IDLE
