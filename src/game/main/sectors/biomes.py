from enum import IntEnum, auto
from typing import Dict

import arcade

from src.game.main.sectors.chunk import Chunk
from src.game.main.sectors.sector_prebuilds.basic_asteroid_chunk import BasicAsteroidChunk
from src.game.main.sectors.sector_prebuilds.basic_enemy_chunk import BasicEnemyChunk
from src.game.main.sectors.sector_prebuilds.biome_specific.asteroid_fields.big_asteroids import BigAsteroidsChunk
from src.game.main.sectors.sector_prebuilds.biome_specific.crimson_void.enemy_fleet import EnemyFleetChunk
from src.game.main.sectors.sector_prebuilds.biome_specific.toxic_wastes.enemy_patrol import EnemyPatrolChunk
from src.game.main.sectors.sector_prebuilds.empty_chunk import EmptyChunk


class Biome(IntEnum):
    ASTEROID_FIELDS = 0, # TODO auto() does not want to work here, why ???
    CRIMSON_VOID = 1, # auto(),
    TOXIC_WASTES = 2, # auto()


BiomeColorTheme: Dict[Biome, arcade.Color] = {
    Biome.ASTEROID_FIELDS: (50, 91, 255),
    Biome.CRIMSON_VOID: (255, 50, 100),
    Biome.TOXIC_WASTES: (50, 255, 100),
}

BiomeChunks: Dict[Biome, list[Chunk]] = None


def get_biome_color_theme(biome: Biome):
    return BiomeColorTheme.get(biome, None)

def get_biome_chunks(biome: Biome):
    global BiomeChunks
    if BiomeChunks is None:
        BiomeChunks = {
            Biome.ASTEROID_FIELDS: [BigAsteroidsChunk(0.08), BasicEnemyChunk(0.2),
                                    BasicAsteroidChunk(0.35, 0.02), BigAsteroidsChunk(0.75), BasicEnemyChunk(0.85),
                                    BigAsteroidsChunk(1)],
            Biome.CRIMSON_VOID: [EmptyChunk(0.05), BasicEnemyChunk(0.15), EnemyFleetChunk(0.35), BasicAsteroidChunk(0.65, 0.01),
                                 BasicEnemyChunk(0.85, 0.015), EnemyFleetChunk(1)],
            Biome.TOXIC_WASTES: [EnemyPatrolChunk(0.1), EmptyChunk(0.15), EnemyPatrolChunk(0.3),
                                 BasicAsteroidChunk(0.5, 0.025), BasicAsteroidChunk(0.65, 0.02), EmptyChunk(0.8),
                                 EnemyPatrolChunk(1, 0.015)]
        }
    return BiomeChunks.get(biome, None)


if __name__ == "__main__":
    pass
