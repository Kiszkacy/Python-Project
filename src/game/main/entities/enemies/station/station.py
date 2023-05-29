from typing import List

from src.game.main.entities.enemies.station.shield_beacon import EnemyStationBeacon
from src.game.main.entities.structure import Structure
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.events.destroy_event import DestroyEvent
from src.game.main.events.event import Event
from src.game.main.events.event_observer import Observer
from src.game.main.interfaces.collidable import Collidable
from src.game.main.singletons.event_register import EventRegister
from src.game.main.util.path_loader import get_absolute_resource_path


class EnemyStation(Structure, Observer):

    def __init__(self) -> None:
        super(EnemyStation, self).__init__(sprite_url=get_absolute_resource_path("\\sprites\\stationary\\station.png"),
                                           mass=1000.0, belongs_to=ObjectCategory.ENEMIES,
                                           collides_with=[ObjectCategory.STATIC, ObjectCategory.PLAYER, ObjectCategory.PROJECTILES, ObjectCategory.ENEMIES],
                                           hp_max=250.0, shd_max=50.0, power_max=1000.0)
        self.invulnerable: bool = True
        self.beacons_killed: int = 0
        self.beacons: List[EnemyStationBeacon] = []
        EventRegister.add_observer(self)

    def damage(self, amount: float) -> float:
        if self.invulnerable: return 0.0
        return super(Structure, self).damage(amount)

    def handle_collisions(self, delta: float) -> List[Collidable]:
        return [] # remove collisions so the object is immovable

    def notify(self, event: Event) -> None:
        if isinstance(event, DestroyEvent) and isinstance(event.destroyed, EnemyStationBeacon):
            for b in self.beacons:
                b.orbit_speed += 0.2 # TODO hardcoded
            self.beacons_killed += 1
            if self.beacons_killed == len(self.beacons): self.invulnerable = False


if __name__ == '__main__':
    pass
