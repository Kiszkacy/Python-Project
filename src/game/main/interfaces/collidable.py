from src.game.main.enums.object_category import ObjectCategory


class Collidable:

    def __init__(self, belongs_to: ObjectCategory, collides_with: list[ObjectCategory]) -> None:
        self.belongs_to: ObjectCategory = belongs_to
        self.collides_with: list[ObjectCategory] = collides_with
        # TODO add here object to EntityHandler list?


if __name__ == '__main__':
    pass
