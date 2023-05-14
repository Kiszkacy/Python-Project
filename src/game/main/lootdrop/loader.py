from typing import Dict, Callable, List

import timeit

from src.game.main.inventory.items import Item
from src.game.main.lootdrop.lootdrop import LootDrop
from src.game.main.util.file_handler import FileHandler
from src.game.main.util.path_loader import get_absolute_resource_path
from src.game.main.lootdrop.methods import RollType, ChanceType


class Loader:

    @staticmethod
    def load_from_json(path: str) -> LootDrop:
        dict: Dict = FileHandler.load_json2dict(path)
        return Loader._load(dict)

    @staticmethod
    def _load(data: dict) -> LootDrop|Item:
        if "entries" in data.keys():
            # entries
            size: int = len(data["entries"])
            entries: List[Item | LootDrop] = [Loader._load(entry) for entry in data["entries"]]

            # roll function
            rolls: Dict = data["rolls"]
            arg_count: int = RollType[rolls["type"]].__code__.co_argcount
            args: List[int] = [rolls[f"arg{i}"] for i in range(arg_count)]
            roll_func: Callable = lambda: RollType[rolls["type"]](*args)

            # chance function
            chance: Dict = data["chance"]
            arg_count = ChanceType[chance["type"]].__code__.co_argcount
            # -1 because size is always needed and its calculated via loader so its not needed in json file
            args = [chance[f"arg{i}"] for i in range(arg_count-1)]
            chance_func: Callable = lambda: ChanceType[chance["type"]](size, *args)

            return LootDrop(entries, roll_func, chance_func)
        else: # Item
            return Item[data["name"]]

if __name__ == '__main__':
    ld: LootDrop = Loader.load_from_json(get_absolute_resource_path("\\enemies\\loottables\\test2.json"))

    start = timeit.default_timer()
    for i in range(10): ld.calc()
    print(timeit.default_timer() - start)

