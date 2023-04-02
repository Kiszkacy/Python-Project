from src.entities.Entity import Entity
from src.singletons.EntityHandler import EntityHandler
from src.interfaces.Collidable import Collidable
from src.auxilary.ObjectCategory import ObjectCategory


class TempWall(Entity, Collidable):

    def __init__(self):
        Entity.__init__(self, sprite_url="..\\resources\\sprites\\tmp_wall.png")
        Collidable.__init__(self, belongs_to=[ObjectCategory.STATIC], collides_with=[])
        EntityHandler.add(self, ObjectCategory.STATIC)
        self.scale = 0.1
