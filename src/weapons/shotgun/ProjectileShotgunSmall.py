
from src.entities.Projectile import Projectile
from src.auxilary.ObjectCategory import ObjectCategory


class ProjectileShotgunSmall(Projectile):

    def __init__(self) -> None:
        Projectile.__init__(self, sprite_url="..\\resources\\sprites\\tmp_projectile4.png",
                            belongs_to=ObjectCategory.PROJECTILES,
                            collides_with=[ObjectCategory.STATIC, ObjectCategory.ENEMIES, ObjectCategory.MISC],
                            damage=8.0,
                            acceleration=-200.0,
                            falloff_damage=[(1.0, 0.0), (0.5, 500.0)])


if __name__ == '__main__':
    pass
