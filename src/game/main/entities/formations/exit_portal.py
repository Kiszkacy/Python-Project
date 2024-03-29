
from src.game.main.entities.formations.formation import Formation
from src.game.main.entities.friendly.portal import Portal


class ExitPortal(Formation):

    def __init__(self) -> None:
        super(ExitPortal, self).__init__(width=200, height=200, entities=[(Portal(), (0,0))])
        self.used = False


if __name__ == '__main__':
    pass
