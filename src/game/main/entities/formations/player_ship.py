
from src.game.main.entities.formations.formation import Formation
from src.game.main.entities.player_ship import PlayerShip


class PlayerSpawn(Formation):

    def __init__(self) -> None:
        super(PlayerSpawn, self).__init__(width=200, height=200, entities=[(PlayerShip(), (0,0))])


if __name__ == '__main__':
    pass
