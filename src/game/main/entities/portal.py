import arcade

from src.game.main.entities.entity import Entity
from src.game.main.entities.player_ship import PlayerShip
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.util.path_loader import get_absolute_resource_path


class Portal(Entity):

    def __init__(self) -> None:
        super(Portal, self).__init__(sprite_url=get_absolute_resource_path("\\sprites\\stationary\\exit_portal.png"))
        self.player_ship: PlayerShip = EntityHandler.player

    def on_update(self, delta_time: float = 1 / 60) -> None:
        if arcade.get_distance(self.player_ship.position[0], self.player_ship.position[1], self.position[0], self.position[1]) < 400.0: # TODO hardcoded
            pass # TODO here register event


if __name__ == '__main__':
    pass
