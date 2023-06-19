
from src.game.main.entities.asteroids.medium import AsteroidMedium
from src.game.main.entities.formations.formation import Formation


class MinableAsteroid(Formation):

    def __init__(self) -> None:
        asteroid: AsteroidMedium = AsteroidMedium((0,0), (0,0))
        asteroid.minable = True
        super(MinableAsteroid, self).__init__(width=80, height=80, entities=[(asteroid, (0,0))])


if __name__ == '__main__':
    pass
