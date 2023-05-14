from src.game.main.behaviors.behavior import Behavior
from src.game.main.behaviors.finite_state_machine import FiniteStateMachine
from src.game.main.behaviors.states.attacking_state import AttackingState
from src.game.main.behaviors.states.calm_state import CalmState
from src.game.main.entities.ship import Ship
from src.game.main.singletons.entity_handler import EntityHandler


def basic_enemy_behavior(body: Ship) -> Behavior:
    calm = CalmState(body)
    behavior = FiniteStateMachine(calm, [AttackingState(body, calm, EntityHandler.player)], resumable=True)
    return behavior
