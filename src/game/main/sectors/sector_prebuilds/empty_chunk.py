from arcade import SpriteList
from src.game.main.sectors.chunk import Chunk


class EmptyChunk(Chunk):

    def __init__(self, cumulative_prob, density: float = 0.005):
        super().__init__(density, [], cumulative_prob)


    def generate(self, left_corner: tuple[int, int]):
        """
        Empty chunk, nothing is generated
        :param left_corner:
        :return:
        """
        pass
