from src.game.main.entities.object import Object
from src.game.main.enums.object_category import ObjectCategory


class Structure(Object):
    # TODO move this to config file?
    POWER_TICKS_PER_SECOND: int = 4
    POWER_REGEN_COOLDOWN: float = 1.0 / POWER_TICKS_PER_SECOND

    def __init__(self, sprite_url: str, mass: float, belongs_to: ObjectCategory, collides_with: list[ObjectCategory],
                 hp_max: float = 100.0, shd_max: float = 25.0,
                 power_max: float = 100.0, power_regen_amount: float = 25.0,
                 power_regen_delay: float = 2.5) -> None:
        super(Structure, self).__init__(sprite_url, mass, belongs_to, collides_with, hp_max, shd_max)
        self.power_max: float = power_max
        self.power_regen_amount: float = power_regen_amount
        self.power_regen_delay: float = power_regen_delay
        # SCRIPT VARS "PRIVATE"
        self.power: float = self.power_max # PLEASE USE SETTER ON ME THANKS
        self.power_timer: float = 0.0
        self.power_regenerating: bool = False
        self.power_timer_online: bool = False

    def on_update(self, delta_time: float = 1 / 60) -> None:
        super(Structure, self).on_update(delta_time)
        # update power timer
        if self.power_timer_online:
            self.power_timer -= delta_time
            if self.power_timer <= 0.0:
                self.power_regen()

    def power_regen(self) -> None:
        if self.power >= self.power_max: # stop when at max power
            self.power_regenerating = False
            self.power_timer_online = False
            return
        self.power_regenerating = True
        self.power = min(self.power_max, self.power + self.power_regen_amount * Structure.POWER_REGEN_COOLDOWN)
        self.power_timer = Structure.POWER_REGEN_COOLDOWN

    def power_regen_request(self) -> None:
        self.power_timer_online = True
        self.power_regenerating = False
        self.power_timer = self.power_regen_delay

    def set_power(self, to: float) -> None:
        if to < self.power:
            self.power_regen_request()
        self.power = max(min(to, self.power_max), 0.0)


if __name__ == '__main__':
    pass
