from src.auxilary.ObjectCategory import ObjectCategory


class Collidable:

    def __init__(self, belongs_to: list[ObjectCategory], collides_with: list[ObjectCategory]) -> None:
        self.belongs_to: list[ObjectCategory] = belongs_to
        self.collides_with: list[ObjectCategory] = collides_with
        # TODO add here object to EntityHandler list?
