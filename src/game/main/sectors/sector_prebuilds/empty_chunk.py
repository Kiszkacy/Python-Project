from arcade import SpriteList
from src.game.main.sectors.chunk import Chunk


class EmptyChunk(Chunk):

    def __init__(self, cumulative_prob, density: float = 0.005):
        super().__init__(density, SpriteList(), [], cumulative_prob)
