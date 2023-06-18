import arcade

from src.game.main.entities.entity import Entity
from src.game.main.entities.player_ship import PlayerShip
from src.game.main.events.entering_sector_event import SectorCompleted
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.singletons.event_register import EventRegister
from src.game.main.util.path_loader import get_absolute_resource_path


class Portal(Entity):

    def __init__(self) -> None:
        super(Portal, self).__init__(sprite_url=get_absolute_resource_path("\\sprites\\stationary\\exit_portal.png"))
        self.player_ship: PlayerShip = EntityHandler.player
        self.used = False

    def on_update(self, delta_time: float = 1 / 60) -> None:
        if arcade.get_distance(self.player_ship.position[0], self.player_ship.position[1], self.position[0], self.position[1]) < 200.0: # TODO hardcoded
            EventRegister.register_new(SectorCompleted())
            print("registering event")
            self.used = True


if __name__ == '__main__':
    pass
