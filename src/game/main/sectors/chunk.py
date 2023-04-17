import copy
import math
import random
import numpy as np

from arcade import SpriteList

from src.game.main.enums.object_category import ObjectCategory
from src.game.main.singletons.config import Config
from src.game.main.singletons.entity_handler import EntityHandler


class Chunk:

    def __init__(self, density: float, objects: SpriteList, probabilities: list[float], cumulative_probability):
        """

        :param density: Density of objects in the chunk
        :param objects: Sprite list of objects from witch we will be drawing objects to place
        :param probabilities: Probability of each objects to be drawn, should be in the same order as objects
        """
        self.density: float = density
        self.size: int = Config.Constants["CHUNK_SIZE"]
        self.objects: SpriteList = objects
        self.probabilities: list[float] = probabilities
        self.cumulative_probability: float = cumulative_probability

    def _generate(self, left_corner: tuple[int, int]) -> SpriteList:
        if len(self.objects) == 0:
            return SpriteList()

        generated_objects: SpriteList = SpriteList(use_spatial_hash=True)
        avg_area: float = sum(sprite.height * sprite.width * self.probabilities[i] for i, sprite in enumerate(self.objects))
        total_area: int = self.size*self.size
        amount_of_objects: int = math.floor((total_area / avg_area) * self.density)  # approximate amount of objects
        # to reach desired density

        # drawing random objects, with set probability, amount of objects is set to amount_of_objects
        object_choices = np.random.choice(self.objects, amount_of_objects, p=self.probabilities)

        for chosen_object in object_choices:
            unsuccessful_tries = 0  # in case there is no room for next object, because density is too high
            successful = False
            new_object = copy.deepcopy(chosen_object)

            while not successful and unsuccessful_tries < 2:  # depending on performance could be increased
                # making sure that object won't go outside its own chunk
                x = random.randint(new_object.width, self.size-new_object.width) + left_corner[0]
                y = random.randint(new_object.height, self.size-new_object.height) + left_corner[1]
                new_object.position = (x,y)

                if new_object.collides_with_list(generated_objects):
                    unsuccessful_tries += 1
                else:
                    generated_objects.append(new_object)
                    successful = True

        return generated_objects

    def generate(self, left_corner: tuple[int, int]):
        """
        should not be called, it's need to be overwritten for it's child
        :param left_corner: left corner coordinates of chunk
        :return: None
        """
        EntityHandler.add(self._generate(left_corner), ObjectCategory.ENEMIES)
