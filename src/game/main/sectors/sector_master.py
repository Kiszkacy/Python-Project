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

from src.game.main.events.event import Event
from src.game.main.events.event_observer import Observer
from src.game.main.sectors.sector import Sector
import src.game.main.sectors.biomes as biomes
from src.game.main.singletons.event_register import EventRegister
from src.game.main.save.game_save import GameSave

Coordinate = namedtuple("Coordinate", ["x", "y"])


class Node:
    random_generator = random.Random()
    seed: int = 69

    def __init__(self, parents: list[Node] = None, children: list[Node] = None):
        self._hash = Node.random_generator.randint(-10 ** 10, 10 ** 10)
        self.parents: list[Node] = parents if parents is not None else []
        self.children: list[Node] = children if children is not None else []
        # TODO temporary
        biome: biomes.Biome = Node.random_generator.choices(tuple(biomes.Biome), k=1)[0]
        self.sector: Sector = Sector(
            Difficulty.EASY,
            biomes.get_biome_chunks(biome),
            size=Node.random_generator.choices(tuple(SectorSize), k=1)[0],
            biome_type=biome,
            aspect_ratio=1,
            seed=Node.seed
        )

    def add_child(self, child: Node):
        child.parents.append(self)
        if child not in self.children:
            self.children.append(child)

    def add_children(self, children: list[Node]):
        for child in children:
            child.parents.append(self)
        self.children.extend(children)
        self.children = list(set(self.children))

    def __str__(self):
        return f"[children: {len(self.children)}]"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Node):
            return self._hash == other._hash
        return False

    def __hash__(self):
        return self._hash


class SectorMaster(Observer):

    def __init__(self, seed: int):
        self.sector_map: dict[Node, Coordinate] | None = None
        self.sector_dag: Node | None = None  # root
        self.__current_sector_node: Node = None
        self.seed: int = seed
        Node.random_generator = random.Random(seed)
        Node.seed = seed

    def create_dag(self, max_depth=8, max_width=4, avg_connections=3) -> Node:
        levels = [
            [Node() for _ in range(max((math.ceil(max_width / max(abs(depth - max_depth / 2), 1))), 1))]
            for depth in range(max_depth)]

        if len(levels[0]) != 1:
            levels[0] = [Node()]
        if len(levels[-1]) != 1:
            levels[-1] = [Node()]

        normal = NormalDist(avg_connections, max_width - avg_connections)
        generator = np.random.Generator(PCG64(self.seed))
        for i, level in enumerate(levels[:-1]):
            for node in level:
                connections = round(normal.samples(1, seed=self.seed)[0])
                connections = min(connections, len(levels[i + 1])) if connections > 0 else math.ceil(
                    len(levels[i + 1]) / 2)
                node.add_children(generator.choice(levels[i + 1], replace=True, size=connections))

        return levels[0][0]  # root

    def initialize(self, max_depth=8, max_width=4, avg_connections=3):
        self.sector_dag = self.create_dag(max_depth, max_width, avg_connections)
        self.current_sector_node = self.sector_dag
        self.sector_map = self.get_sector_map()
        EventRegister.add_observer(self)

    def get_sector_map(self) -> dict[Node, Coordinate]:
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
            mid_idx = (len(positions) - 1) / 2

            if mid_idx.is_integer():
                positions[round(mid_idx)] = math.floor(positions[round(mid_idx)] * 2) / 2
                sector_map[layer[round(mid_idx)]] = Coordinate(positions[round(mid_idx)], -depth - 1)

            for i in range(1, math.ceil(mid_idx) + 1):
                idx = math.ceil(mid_idx) - i

                if mid_idx >= idx:
                    if len(positions) > idx + 1 and positions[idx + 1] - positions[idx] < 1:
                        positions[idx] += positions[idx + 1] - positions[idx] - 1

                    positions[idx] = math.floor(positions[idx] * 2) / 2
                    sector_map[layer[idx]] = Coordinate(positions[idx], -depth - 1)

                idx = math.floor(mid_idx) + i

                if len(positions) > idx:
                    if abs(positions[idx - 1] - positions[idx]) < 1:
                        positions[idx] += 1 - abs(positions[idx - 1] - positions[idx])
                    positions[idx] = math.ceil(positions[idx] * 2) / 2
                    sector_map[layer[idx]] = Coordinate(positions[idx], -depth - 1)

        self.sector_map = sector_map
        return sector_map

    def _get_average_parent_x(self, node: Node, sector_map: dict[Node, Coordinate]):
        if node.parents:
            sum_of_x_cords = sum(sector_map.get(parent, Coordinate(0, 0)).x for parent in node.parents)
            return sum_of_x_cords / len(node.parents)
        else:
            return 0

    def is_sector_unlocked(self, sector_node: Node) -> bool:
        """Should only be called after calling initialize on sector master"""
        # root, as starting sector is always unlocked
        if sector_node == self.sector_dag: return True

        # if sector is finished it means it was already unlocked
        if sector_node.__hash__() in GameSave.stats["finished_sectors"]: return True

        # if any of our parent sectors was finished, it unlocks its children
        if sum([parent.__hash__() in GameSave.stats["finished_sectors"] for parent in sector_node.parents]): return True

        return False


    def notify(self, event: Event) -> None:
        from src.game.main.events.entering_sector_event import SectorCompleted
        match event:
            case SectorCompleted():
                print("Sector master: Finishd sector")
                print(f"Before: {GameSave.stats}")
                GameSave.stats["finished_sectors"].append(self.current_sector_node.__hash__())
                print(f"After: {GameSave.stats}")

    @property
    def current_sector_node(self) -> Node:
        return self.__current_sector_node

    @current_sector_node.setter
    def current_sector_node(self, value: Node):
        if value is not None:
            self.__current_sector_node = value
        else:
            self.__current_sector_node = value

    @property
    def current_sector(self) -> Sector:
        return self.current_sector_node.sector

    def get_sector_node_by_hash(self, node_hash: int) -> Node | None:
        for elem in self.sector_map.keys():
            if elem.__hash__() == node_hash:
                return elem
