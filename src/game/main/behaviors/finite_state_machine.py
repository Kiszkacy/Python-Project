from src.game.main.behaviors.state import State
from src.game.main.enums.behavior_status import BehaviorStatus


class FiniteStateMachine(State):

    def __init__(self, start_state=None, priority_states=None, context=None,
                 interruptable=False, resumable=False, loop=True):
        super().__init__(context, interruptable, resumable)
        self.state: FiniteStateMachine | State = start_state
        self.start_state: FiniteStateMachine | State = start_state
        self.priority_states: list[FiniteStateMachine | State] = priority_states
        self.back_log: FiniteStateMachine | State = None    #could be a queue
        self.loop = loop


    def priority_checks(self):
        for priority_state in self.priority_states:
            if self.state != priority_state and priority_state.check():
                if self.state.resumable:
                    self.back_log = self.state
                self.state = priority_state
                # TODO return after first successful check?

    def execute(self, delta_time: float = 1 / 60):
        if self.state.interruptable:
            self.priority_checks()

        self.state.execute(delta_time)  # state is executing

        match self.state.status:
            case BehaviorStatus.RUNNING:
                pass
            case BehaviorStatus.NEXT_STATE:
                self.state = self.state.next()  # state.next() returns state with already set context
            case BehaviorStatus.IDLE:   # state finished execution, no next state
                if self.back_log is None:
                    if self.loop:
                        self.state = self.start_state
                    else:
                        self.status = BehaviorStatus.IDLE
                else:
                    self.state = self.back_log

    def reset(self, context):
        self.back_log = None
        self.state = self.start_state
        self.state.reset(context)
