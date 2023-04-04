
from src.entities.Projectile import Projectile
from src.auxilary.ObjectCategory import ObjectCategory


class ProjectileAura(Projectile):

    def __init__(self) -> None:
        Projectile.__init__(self, sprite_url="..\\resources\\sprites\\tmp_projectile3.png",
                            belongs_to=ObjectCategory.PROJECTILES, collides_with=[ObjectCategory.STATIC, ObjectCategory.ENEMIES],
                            acceleration=350.0,
                            lifetime=1.8)


if __name__ == '__main__':
    pass
