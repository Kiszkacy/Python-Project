from src.game.main.entities.entity import Entity
from src.game.main.util.path_loader import get_absolute_resource_path


class Portal(Entity):

    def __init__(self) -> None:
        super(Portal, self).__init__(sprite_url=get_absolute_resource_path("\\sprites\\stationary\\exit_portal.png"))

    def on_update(self, delta_time: float = 1 / 60) -> None:
        pass # TODO check distance to player


if __name__ == '__main__':
    pass
