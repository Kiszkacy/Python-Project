
from src.entities.projectiles.Projectile import Projectile
from src.singletons.CollisionHandler import CollisionHandler
from src.interfaces.Collidable import Collidable
from src.auxilary.ObjectCategory import ObjectCategory
from src.singletons.EntityHandler import EntityHandler


class TempProjectile(Projectile, Collidable):

    def __init__(self) -> None:
        Projectile.__init__(self, sprite_url="..\\resources\\sprites\\tmp_projectile.png")
        Collidable.__init__(self, belongs_to=[ObjectCategory.PROJECTILES], collides_with=[ObjectCategory.STATIC])
        # TODO maybe add here to entity handler
        # EntityHandler.add(self, ObjectCategory.PROJECTILES)

    def on_update(self, delta_time: float = 1 / 60) -> None:
        super(TempProjectile, self).on_update(delta_time)
        hit_list = CollisionHandler.check_collision(self)
        if hit_list:
            self.kill()


if __name__ == '__main__':
    pass
