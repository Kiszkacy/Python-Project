from src.game.main.entities.entity import Entity
from src.game.main.movement.movement_type import MovementType


class LinearMovement(MovementType):

    def __init__(self) -> None:
        super(LinearMovement, self).__init__()

    def move(self, delta: float, object: Entity) -> None:
        object.position = (object.position[0] + object.velocity[0]*delta, object.position[1] + object.velocity[1]*delta)



if __name__ == '__main__':
    pass
