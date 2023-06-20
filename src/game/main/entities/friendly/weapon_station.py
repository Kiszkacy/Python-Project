import random
from typing import List, Optional

import arcade

from src.game.main.entities.structure import Structure
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.events.event import Event
from src.game.main.events.event_observer import Observer
from src.game.main.events.interact_event import InteractEvent
from src.game.main.interfaces.collidable import Collidable
from src.game.main.level.progress_functions import weapon_unlocks_for, calculate_level
from src.game.main.singletons.config import Config
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.singletons.event_register import EventRegister
from src.game.main.singletons.player_statistics import PlayerStatistics
from src.game.main.util.path_loader import get_absolute_resource_path
from src.game.main.weapons.weapon import Weapon


class WeaponStation(Structure, Observer):

    def __init__(self) -> None:
        super(WeaponStation, self).__init__(sprite_url=get_absolute_resource_path("\\sprites\\stationary\\friendly_station.png"),
                                           mass=1000.0, belongs_to=ObjectCategory.FRIENDLY,
                                           collides_with=[],
                                           hp_max=250.0, shd_max=50.0, power_max=1000.0)
        self.interact_range: float = 256.0
        self.active: bool = False
        self.weapon: Optional[Weapon] = random.choice(weapon_unlocks_for(calculate_level(PlayerStatistics.stats['exp'])))
        EventRegister.add_observer(self)

    def on_update(self, delta_time: float = 1 / 60) -> None:
        super().on_update(delta_time)
        if self.active and arcade.get_distance(self.position[0], self.position[1], EntityHandler.player.position[0], EntityHandler.player.position[1]) > self.interact_range:
            self.active = False

        if self.active:
            print(self.weapon.name)

    def handle_collisions(self, delta: float) -> List[Collidable]:
        return [] # remove collisions so the object is immovable

    def notify(self, event: Event) -> None:
        if isinstance(event, InteractEvent):
            if arcade.get_distance(self.position[0], self.position[1], event.at[0], event.at[1]) > self.interact_range: return
            if self.active:
                if EntityHandler.player.weapon_count == Config.Constants.get("WEAPONS_MAX"): return
                EntityHandler.player.weapon_count += 1
                EntityHandler.player.weapons.append(self.weapon)
                self.weapon = None
                self.active = False
            elif self.weapon is not None:
                self.active = True


if __name__ == '__main__':
    pass
