from __future__ import annotations
import math
import random
from statistics import NormalDist
from matplotlib import pyplot as plt
from collections import namedtuple
import numpy as np
from numpy.random import PCG64

from src.game.main.enums.difficulty import Difficulty
from src.game.main.enums.sector_size import SectorSize
from src.game.main.sectors.sector import Sector
import src.game.main.sectors.biomes as biomes


Coordinate = namedtuple("Coordinate", ["x", "y"])

class Node:
    rd = random.Random()
    def __init__(self, parents: list[Node] = None, children: list[Node] = None):
        self._hash = Node.rd.randint(-10 ** 10, 10 ** 10)
        self.parents: list[Node] = parents if parents is not None else []
        self.children: list[Node] = children if children is not None else []
        # TODO temporary
        biome: biomes.Biome = random.choice(list(biomes.Biome))
        self.sector: Sector = Sector(Difficulty.EASY, biomes.get_biome_chunks(biome),
                                     size=random.choice(list(SectorSize)), biome_type=biome, aspect_ratio=1, seed=11)

    def add_child(self, child: Node):
        child.parents.append(self)
        if child not in self.children:
            self.children.append(child)

    def add_children(self, children: list[Node]):
        for child in children: child.parents.append(self)
        self.children.extend(children)
        self.children = list(set(self.children))

    def __str__(self):
        return f"[children: {len(self.children)}]"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Node):
            # return self.children == other.children and self.sector == other.sector
            return self._hash == other._hash
        return False

    def __hash__(self):
        # return hash(tuple(self.children)) ^ hash(self.sector)
        # print(self.__hash)
        return self._hash


class SectorMaster:

    def __init__(self):
        self.sector_map = None
        self.sector_dag = None
        self.current_sector: Sector = None

    def create_dag(self, max_depth=8, max_width=4, avg_connections=3):
        levels = [
            [Node() for _ in range(random.randint(1, max(-(math.floor((depth - max_depth / 2) ** 2)) + max_width, 1)))]
            for depth in range(max_depth)]

        if len(levels[0]) != 1:
            levels[0] = [Node()]
        if len(levels[-1]) != 1:
            levels[-1] = [Node()]

        normal = NormalDist(avg_connections, max_width - avg_connections)
        generator = np.random.Generator(PCG64())
        for i, level in enumerate(levels[:-1]):
            for node in level:
                connections = round(normal.samples(1)[0])
                connections = min(connections, len(levels[i + 1])) if connections > 0 else math.ceil(
                    len(levels[i + 1]) / 2)
                node.add_children(generator.choice(levels[i + 1], replace=True, size=connections))

        plt.scatter([i for level in levels for i in range(len(level))],
                    [y for y in range(len(levels)) for _ in range(len(levels[y]))])
        plt.show()
        return levels[0][0]

    def initialize(self, max_depth=8, max_width=4, avg_connections=3):
        self.sector_dag = self.create_dag(max_depth, max_width, avg_connections)
        self.current_sector = self.sector_dag.sector
        self.sector_map = self.get_sector_map()

    def get_sector_map(self):
        if self.sector_dag is None:
            return None
        if self.sector_map is not None:
            return self.sector_map

        sector_map: dict[Node, Coordinate] = {}
        layers: list[list[Node]] = []

        def get_layers(root: Node, depth=0):
            if len(layers) <= depth:
                layers.append([root])
            else:
                layers[depth].append(root)

            for child in root.children: get_layers(child, depth + 1)

        get_layers(self.sector_dag)
        sector_map[self.sector_dag] = Coordinate(0, 0)  # root

        for depth, layer in enumerate(layers[1:]):
            layer = list(set(layer))
            layer.sort(key=lambda x: self._get_average_parent_x(x, sector_map))
            positions = [self._get_average_parent_x(node, sector_map) for node in layer]
            mid_idx = len(positions)//2
            print(f"layer: {layer}\npositions:{positions}\ndepth: {-depth-1} mid_idx: {mid_idx}\n")

            for i in range(mid_idx+1):
                if mid_idx >= i:
                    if len(positions) > mid_idx-i+1 and positions[mid_idx-i+1] - positions[mid_idx-i] < 1:
                        positions[mid_idx-i] += positions[mid_idx-i+1] - positions[mid_idx-i] - 1
                    print(f"before rouding: {positions[mid_idx-i]}\n")
                    positions[mid_idx-i] = math.floor(positions[mid_idx-i]*2)/2
                    sector_map[layer[mid_idx-i]] = Coordinate(positions[mid_idx-i], -depth-1)
                    print(f"Depth: {-depth - 1}, left i: {mid_idx - i} hash: {layer[mid_idx-i]._hash} pos: {sector_map[layer[mid_idx-i]]}\n")

                if len(positions) > mid_idx+i and i != 0:
                    if abs(positions[mid_idx+i-1] - positions[mid_idx+i]) < 1:
                        positions[mid_idx+i] += 1 - abs(positions[mid_idx+i-1] - positions[mid_idx+i])
                    positions[mid_idx - i] = math.ceil(positions[mid_idx - i] * 2) / 2
                    sector_map[layer[mid_idx+i]] = Coordinate(positions[mid_idx+i], -depth - 1)
                    print(f"Depth: {-depth-1}, right i: {mid_idx+i} hash: {layer[mid_idx+i]._hash} pos: {sector_map[layer[mid_idx+i]]}\n")

        self.sector_map = sector_map
        return sector_map


    def _get_average_parent_x(self, node: Node, sector_map: dict[Node, Coordinate]):
        if node.parents:
            sum_of_x_cords = 0
            for parent in node.parents:
                sum_of_x_cords += sector_map.get(parent, Coordinate(0,0)).x

            return sum_of_x_cords/len(node.parents)
        else:
            return 0
