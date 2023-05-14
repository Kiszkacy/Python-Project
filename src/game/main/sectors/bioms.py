from enum import IntEnum, auto
from typing import Dict

import arcade

from src.game.main.sectors.chunk import Chunk
from src.game.main.sectors.sector_prebuilds.basic_asteroid_chunk import BasicAsteroidChunk
from src.game.main.sectors.sector_prebuilds.basic_enemy_chunk import BasicEnemyChunk
from src.game.main.sectors.sector_prebuilds.empty_chunk import EmptyChunk


class Biom(IntEnum):
    biom1 = 0,
    biom2 = auto()


BiomColorTheme: Dict[Biom, arcade.Color] = {
    Biom.biom1: (255, 50, 100),
    Biom.biom2: (50, 255, 100),
}

BiomChunks: Dict[Biom, list[Chunk]] = None


def get_biom_color_theme(biom: Biom):
    return BiomColorTheme.get(biom, None)


def get_biom_chunks(biom: Biom):
    global BiomChunks
    if BiomChunks is None:
        BiomChunks = {
            Biom.biom1: [EmptyChunk(0.1), BasicEnemyChunk(0.3), BasicAsteroidChunk(1, 0.02)],
            Biom.biom2: [BasicEnemyChunk(-.5), EmptyChunk(0.1), BasicEnemyChunk(0.3), BasicAsteroidChunk(0.9, 0.01),
                         BasicEnemyChunk(1, 0.1)]
        }
    return BiomChunks.get(biom, None)


if __name__ == "__main__":
    pass
