
from src.auxilary.MovementType import MovementType
from src.entities.Entity import Entity


class LinearMovement(MovementType):

    def __init__(self) -> None:
        super(LinearMovement, self).__init__()

    def move(self, delta: float, object: Entity) -> None:
        object.position = (object.position[0] + object.velocity[0] * delta, object.position[1] + object.velocity[1] * delta)



if __name__ == '__main__':
    pass
