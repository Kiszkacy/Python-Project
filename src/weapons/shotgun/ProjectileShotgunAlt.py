
from src.entities.Projectile import Projectile
from src.auxilary.ObjectCategory import ObjectCategory


class ProjectileShotgunAlt(Projectile):

    def __init__(self) -> None:
        Projectile.__init__(self, sprite_url="..\\resources\\sprites\\tmp_projectile2.png",
                            belongs_to=ObjectCategory.PROJECTILES,
                            collides_with=[ObjectCategory.STATIC, ObjectCategory.ENEMIES, ObjectCategory.MISC],
                            damage=12.0,
                            acceleration=-400.0,
                            lifetime=3.0)


if __name__ == '__main__':
    pass
