from time import sleep

from src.game.main.effects.active.active_effect import ActiveEffect
from src.game.main.entities.ship import Ship
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.interfaces.affectable import Affectable
from src.game.main.interfaces.damageable import Damageable
from src.game.main.util.path_loader import get_absolute_resource_path


class DamageEffect(ActiveEffect):

    def __init__(self, target: Affectable, lifetime: float, damage_per_tick: float, ticks_per_sec: int = 4) -> None:
        super(DamageEffect, self).__init__(target, lifetime, ticks_per_sec)
        self.damage_per_tick: float = damage_per_tick
        self.ticks_per_sec: int = ticks_per_sec
        self.tick_delay: float = 1.0 / self.ticks_per_sec

    def activate(self) -> bool:
        if not isinstance(self.target, Damageable):
            return False
        return super(DamageEffect, self).activate()

    def action(self) -> None:
        self.target.damage(self.damage_per_tick)
        self.reset_timer()


if __name__ == '__main__':
    pass

    # obj: Ship = Ship(get_absolute_resource_path("\\sprites\\tmp_ship0.png"), 0.0, ObjectCategory.STATIC, collides_with=[],
    #              hp_max = 100.0, shd_max = 25.0)
    #
    # effect: DamageEffect = DamageEffect(obj, damage_per_tick=1.0, ticks_per_sec=6)
    # effect.activate()
    #
    # while True:
    #     obj.on_update()
    #     print(obj.hp, obj.shd)
    #     sleep(0.017)
