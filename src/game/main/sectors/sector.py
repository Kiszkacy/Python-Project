import math
import random
from typing import List, Optional

import arcade
import matplotlib
import numpy as np
import noise
import seaborn as sns
from matplotlib import pyplot as plt

from src.game.main.entities.formations.rival_station import RivalStation
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.quests.quest import Quest
from src.game.main.quests.quest_mapping import QuestConstructor, MainQuests, SideQuests
from src.game.main.quests.quest_type import QuestType
from src.game.main.sectors import chunk, biomes
from src.game.main.singletons.config import Config
from src.game.main.enums.difficulty import Difficulty
from src.game.main.enums.sector_size import SectorSize
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.util.rand import one_in


class Sector:

    def __init__(self, difficulty: Difficulty, chunks: list[chunk], size: SectorSize, biome_type: biomes.Biome,
                 aspect_ratio: float = 1, seed: int | float = 0):
        """
        :param difficulty: used to generate quest data
        :param chunks: list of chunks from witch the world will be generated
        :param size: amount of chunks inside the sector
        :param aspect_ratio: aspect_ratio of generated sector width/height
        :param seed: seed used for generation
        """
        self.difficulty: Difficulty = difficulty
        self.grid_size: int = Config.Constants["CHUNK_SIZE"]
        self.type: biomes.Biome = biome_type
        self.seed: int = seed
        self.chunks: list[chunk] = chunks
        self.chunks.sort(key=lambda x: x.cumulative_probability)
        self.size: SectorSize = size
        self.height: int = math.floor(math.sqrt(size.value / aspect_ratio)) # amount of chunks
        self.width: int = math.ceil(self.height*aspect_ratio) # amount of chunks
        self.grid: np.array = None
        self.main_quest: Quest = None
        self.side_quest: Quest = None
        random.seed(seed)

    # NOTE: here sector should generate its biome and quest type
    # TODO: biome generation here
    def pre_generate(self) -> None:
        self.main_quest = QuestConstructor.get(random.choice(MainQuests))()
        self.main_quest.generate(self.difficulty, self.seed)

        self.side_quest = QuestConstructor.get(random.choice(SideQuests))()
        self.side_quest.generate(self.difficulty, self.seed)


    def generate(self, left_corner=(0, 0)):
        """
        Generates objects in given area
        :param left_corner: Left corner of the area in which generation will take place
        :return: None
        """

        grid = np.zeros((self.width, self.height), dtype=float)
        scale = 10.0
        octaves = 6
        persistence = 0.5
        lacunarity = 2.0
        ofsett_x = random.randint(-1000, 1000)
        ofsett_y = random.randint(-1000, 1000)

        for i in range(self.width):
            for j in range(self.height):
                grid[i][j] = noise.pnoise2(i / scale + ofsett_x,
                                           j / scale + ofsett_y,
                                           octaves=octaves,
                                           persistence=persistence,
                                           lacunarity=lacunarity,
                                           repeatx=1024,
                                           repeaty=1024,
                                           base=0)

        # normalizing the values
        grid = ((grid - np.min(grid)) / (np.max(grid) - np.min(grid)))
        for i in range(self.width):
            for j in range(self.height):
                current_chunk = None
                for k, elem in enumerate(self.chunks):
                    if elem.cumulative_probability >= grid[i][j]:
                        current_chunk = elem
                        grid[i][j] = k
                        break
                if current_chunk is None: continue
                current_chunk.generate((left_corner[0] + i * self.grid_size, left_corner[1] + j * self.grid_size))

        # create pathfinding tree
        EntityHandler.update_barrier_list(self.width, self.height)

        # place formations

        self.generate_formations()

        self.grid = grid.T
        ax: matplotlib.axes.Axes = sns.heatmap(self.grid, annot=True)
        ax.invert_yaxis()
        plt.show()

    def generate_formations(self) -> None:
        print("YEP")
        if one_in(2): pass # generate friendly trading station
        # generate item trade station
        # generate enemy station if quest needs it
        if self.main_quest.type_ == QuestType.DESTROY_STATION:
            print("AHA")
            formation: RivalStation = RivalStation()
            pos: Optional[arcade.Point] = None
            # loops until valid position is found
            while pos is None:
                pos = self.find_empty_space(formation.width, formation.height, 1000)
            formation.place(pos, ObjectCategory.ENEMIES, True)
            print(pos)


    def find_empty_space(self, width, height, max_tries=20,
                         categories: List[ObjectCategory] = (ObjectCategory.ENEMIES, ObjectCategory.STATIC, ObjectCategory.PLAYER, ObjectCategory.NEUTRAL)) -> Optional[arcade.Point]:
        """
        finds empty space on the map
        :param width: Width of the searched area
        :param height: Height of the searched area
        :param max_tries: Max amount of searches for the empty area
        :param categories: Categories of witch objects area should be empty
        :return: Coordinates of the center of rectangle found or empty tuple
        """
        dummy_sprite = arcade.Sprite(texture=arcade.Texture.create_filled("dummy texture", (width, height), (0,0,0,0)))
        chunk_size = Config.Constants["CHUNK_SIZE"]

        for _ in range(max_tries):
            position = (random.randint(0, self.width*chunk_size), random.randint(0, self.height*chunk_size))
            dummy_sprite.set_position(*position)

            for category in categories:
                if len(dummy_sprite.collides_with_list(EntityHandler.categorized[category])) != 0:
                    break
            else:   # no collision detected
                return position
        return None   # no empty space
