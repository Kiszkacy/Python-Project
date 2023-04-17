import math
import random

import matplotlib
import numpy as np
import noise
import seaborn as sns
from matplotlib import pyplot as plt

from src.game.main.enums.object_category import ObjectCategory
from src.game.main.sectors import chunk
from src.game.main.singletons.config import Config
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.enums.difficulty import Difficulty
from src.game.main.enums.sector_size import SectorSize


class Sector:

    def __init__(self, difficulty: Difficulty, chunks: list[chunk], size: SectorSize,
                 aspect_ratio: float = 1, seed: int | float = 0):
        """
        :param difficulty: Does nothing for now
        :param chunks: list of chunks from witch the world will be generated
        :param size: amount of chunks inside the sector
        :param aspect_ratio: aspect_ratio of generated sector width/height
        :param seed: seed used for generation
        """
        self.difficulty: Difficulty = difficulty
        self.grid_size: int = Config.Constants["CHUNK_SIZE"]
        self.seed: int = seed
        self.chunks: list[chunk] = chunks
        self.chunks.sort(key=lambda x: x.cumulative_probability)
        self.size: SectorSize = size
        self.height: int = math.floor(math.sqrt(size.value / aspect_ratio))
        self.width: int = math.ceil(self.height*aspect_ratio)
        self.grid: np.array = None
        random.seed(seed)

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
        grid = (grid / np.max(
            grid))  # * max(self.chunks, key=lambda x: x.cumulative_probability).cumulative_probability
        for i in range(self.width):
            for j in range(self.height):
                current_chunk = None
                for k, elem in enumerate(self.chunks):
                    print(i, j)
                    if elem.cumulative_probability >= grid[i][j]:
                        current_chunk = elem
                        grid[i][j] = k
                        break
                if current_chunk is None: continue
                current_chunk.generate((left_corner[0] + i * self.grid_size, left_corner[1] + j * self.grid_size))

        self.grid = grid.T
        ax: matplotlib.axes.Axes = sns.heatmap(self.grid, annot=True)
        ax.invert_yaxis()
        plt.show()
