
class Damageable:
    # TODO move this to config file?
    SHIELD_TICKS_PER_SECOND: int = 4
    SHIELD_REGEN_COOLDOWN: float = 1.0 / SHIELD_TICKS_PER_SECOND
    SHIELD_REGEN_DELAY: float = 5.0

    def __init__(self, hp_max: float = 100.0, shd_max: float = 25.0, hp: float = -1.0, shd: float = -1.0) -> None:
        self.hp: float = hp_max if hp < 0.0 else hp
        self.hp_max: float = hp_max
        self.shd: float = shd_max if shd < 0.0 else shd # PLEASE USE SETTER ON ME THANKS
        self.shd_max: float = shd_max
        # script vars
        self.shield_timer: float = 0.0
        self.shield_regenerating: bool = False
        self.shield_timer_online: bool = False

    # damages self by given amount
    # returns real damage dealt
    def damage(self, amount: float) -> float:
        if self.shd > amount:
            self.set_shield(self.shd - amount)
        elif self.shd > 0.0: # and self.shd <= amount
            amount = self.shd
            self.set_shield(0.0)
        elif self.hp > amount:
            self.shield_regen_request() # reset shield regen cd
            self.hp -= amount
        else:
            self.shield_regen_request() # reset shield regen cd
            amount = self.hp
            self.hp = 0.0

        return amount


    def shield_regen(self) -> None:
        if self.shd >= self.shd_max: # stop when at max shd
            self.shield_regenerating = False
            self.shield_timer_online = False
            return
        self.shield_regenerating = True
        self.shd = min(self.shd_max, self.shd + Damageable.SHIELD_REGEN_DELAY * Damageable.SHIELD_REGEN_COOLDOWN)
        self.shield_timer = Damageable.SHIELD_REGEN_COOLDOWN


    def shield_regen_request(self) -> None:
        self.shield_timer_online = True
        self.shield_regenerating = False
        self.shield_timer = Damageable.SHIELD_REGEN_DELAY


    def set_shield(self, to: float) -> None:
        if to < self.shd:
            self.shield_regen_request()
        self.shd = max(min(to, self.shd_max), 0.0)


if __name__ == '__main__':
    pass
