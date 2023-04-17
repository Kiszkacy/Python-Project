import matplotlib
import numpy as np
import noise
import seaborn as sns
from matplotlib import pyplot as plt

from src.game.main.enums.object_category import ObjectCategory
from src.game.main.sectors import chunk
from src.game.main.singletons.config import Config
from src.game.main.singletons.entity_handler import EntityHandler


class Sector:

    def __init__(self, difficulty: float, chunks: list[chunk], width: int = 10, height: int = 10):
        """
        :param difficulty: Does nothing for now
        :param chunks: list of chunks from witch the world will be generated
        :param width: with of the area in grid_size
        :param height: height of the area in grid_size
        """
        self.difficulty: float = difficulty
        self.grid_size: int = Config.Constants["CHUNK_SIZE"]
        # self.seed: int = seed
        self.chunks: list[chunk] = chunks
        self.chunks.sort(key=lambda x: x.cumulative_probability)
        self.width: int = width
        self.height: int = height
        self.grid: np.array = None

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

        for i in range(self.width):
            for j in range(self.height):
                grid[i][j] = noise.pnoise2(i / scale,
                                           j / scale,
                                           octaves=octaves,
                                           persistence=persistence,
                                           lacunarity=lacunarity,
                                           repeatx=1024,
                                           repeaty=1024,
                                           base=0)

        # setting maximum value in grid equal to cumulative probability max
        grid = (grid / np.max(grid)) #* max(self.chunks, key=lambda x: x.cumulative_probability).cumulative_probability
        for i in range(self.width):
            for j in range(self.height):
                current_chunk = None
                for k, elem in enumerate(self.chunks):
                    print(i,j)
                    if elem.cumulative_probability >= grid[i][j]:
                        current_chunk = elem
                        grid[i][j] = k
                        break
                if current_chunk is None: continue
                l = current_chunk.generate((left_corner[0] + i*self.grid_size, left_corner[1] + j*self.grid_size))
                EntityHandler.add(l, ObjectCategory.ENEMIES)

        self.grid = grid
        ax: matplotlib.axes.Axes = sns.heatmap(grid, annot=True)
        ax.invert_yaxis()
        plt.show()
