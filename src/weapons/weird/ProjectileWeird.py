
from src.entities.Projectile import Projectile
from src.auxilary.ObjectCategory import ObjectCategory


class ProjectileWeird(Projectile):

    def __init__(self) -> None:
        Projectile.__init__(self, sprite_url="..\\resources\\sprites\\tmp_projectile2.png",
                            belongs_to=[ObjectCategory.PROJECTILES], collides_with=[ObjectCategory.STATIC, ObjectCategory.ENEMIES],
                            acceleration=-150.0)


if __name__ == '__main__':
    pass
