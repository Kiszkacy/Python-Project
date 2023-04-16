from src.game.main.entities.entity import Entity
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.interfaces.collidable import Collidable
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.util.path_loader import get_absolute_resource_path


class TempWall(Entity, Collidable):

    def __init__(self):
        Entity.__init__(self, sprite_url=get_absolute_resource_path("\\sprites\\tmp_wall.png"))
        Collidable.__init__(self, belongs_to=ObjectCategory.STATIC, collides_with=[])
        EntityHandler.add(self, ObjectCategory.STATIC)
        self.scale = 0.1
