import math
import random
from statistics import NormalDist
from matplotlib import pyplot as plt

import numpy as np

from src.game.main.enums.difficulty import Difficulty
from src.game.main.enums.sector_size import SectorSize
from src.game.main.sectors.sector import Sector
import src.game.main.sectors.biomes as biomes

class Node:

    def __init__(self, children=None):
        if children is None:
            children = []
        self.children = children
        # TODO temporary
        self.sector: Sector = Sector(Difficulty.EASY, biomes.get_biome_chunks(biomes.Biome.ASTEROID_FIELDS),
                                     size=SectorSize.SMALL, biome_type=biomes.Biome.TOXIC_WASTES, aspect_ratio=1, seed=11)

    def __str__(self):
        return f"children: {len(self.children)}"

    def __repr__(self):
        return self.__str__()


class SectorMaster:

    def __init__(self):
        self.sector_dag = None
        self.current_sector: Sector = None


    def create_dag(self, max_depth=8, max_width=4, avg_connections=3):
        levels = [[Node() for _ in range(random.randint(1, max(-(math.floor((depth-max_depth/2)**2))+max_width, 1)))]
                  for depth in range(max_depth)]

        if len(levels[0]) != 1:
            levels[0] = [Node()]
        if len(levels[-1]) != 1:
            levels[-1] = [Node()]

        normal = NormalDist(avg_connections, max_width-avg_connections)
        for i, level in enumerate(levels[:-1]):
            for node in level:
                connections = round(normal.samples(1)[0])
                connections = min(connections, len(levels[i+1])) if connections > 0 else math.ceil(len(levels[i+1])/2)
                node.children = np.random.choice(levels[i+1], replace=True, size=connections)

        print(levels)
        plt.scatter([i for level in levels for i in range(len(level))], [y for y in range(len(levels)) for _ in range(len(levels[y]))])
        plt.show()
        return levels[0][0]


    def initialize(self, max_depth=8, max_width=4, avg_connections=3):
        self.sector_dag = self.create_dag(max_depth, max_width, avg_connections)
        self.current_sector = self.sector_dag.sector

