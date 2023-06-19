from __future__ import annotations

from src.game.main.entities.collidable_entity import CollidableEntity
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.events.destroy_event import DestroyEvent
from src.game.main.interfaces.affectable import Affectable
from src.game.main.interfaces.damageable import Damageable
from src.game.main.interfaces.destroyable import Destroyable
from src.game.main.singletons.event_register import EventRegister


class Object(CollidableEntity, Damageable, Destroyable, Affectable):

    def __init__(self, sprite_url: str, mass: float, belongs_to: ObjectCategory, collides_with: list[ObjectCategory],
                 hp_max: float, shd_max: float) -> None:
        CollidableEntity.__init__(self, sprite_url, mass, belongs_to, collides_with)
        Damageable.__init__(self, hp_max, shd_max)
        Affectable.__init__(self)
        self.mass: float = mass

    def on_update(self, delta_time: float = 1 / 60) -> None:
        super(Object, self).on_update(delta_time)
        # update shield timer
        if self.shield_timer_online:
            self.shield_timer -= delta_time
            if self.shield_timer <= 0.0:
                self.shield_regen()
        # update effects
        for e in self.effects: e.process(delta_time)

    def damage(self, amount: float) -> float:
        dealt: float = super(Object, self).damage(amount)
        if self.hp <= 0.0 and dealt != 0.0: # != 0.0 to check if not dead already
            self.destroy()
        return dealt

    def destroy(self) -> Destroyable:
        self.kill()
        EventRegister.register_new(DestroyEvent(self))
        return self

    def out_of_bounds(self) -> None:
        self.destroy()
