
class Damageable:

    def __init__(self, max_hp: float = 100.0, max_shd: float = 25.0, hp: float = -1.0, shd: float = -1.0) -> None:
        self.hp: float = max_hp if hp < 0.0 else hp
        self.shd: float = max_shd if shd < 0.0 else shd

    # damages self by given amount
    # returns real damage dealt
    def damage(self, amount: float) -> float:
        if self.shd > amount:
            self.shd -= amount
        elif self.shd > 0.0: # and self.shd <= amount
            amount = self.shd
            self.shd = 0.0
        elif self.hp > amount:
            self.hp -= amount
        else:
            amount = self.hp
            self.hp = 0.0

        return amount


if __name__ == '__main__':
    pass
