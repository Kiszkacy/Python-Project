from dataclasses import dataclass
import random as r

from src.game.main.enums.difficulty import Difficulty
from src.game.main.inventory.items import Item
from src.game.main.quests.quest import Quest
from src.game.main.quests.quest_type import QuestType
from src.game.main.util.rand import randrange


@dataclass
class QuestGatherOre(Quest):
    type_ = QuestType.GATHER_ORE # TODO does not work in dataclass like that
    amount_needed: int = 0
    ore_type: Item = Item.GOLD_ORE

    def generate(self, difficulty: Difficulty = Difficulty.MEDIUM, seed: int = 0) -> None:
        self.type_ = QuestType.GATHER_ORE # TODO tmp fix
        self.ore_type = r.choice([Item.GOLD_ORE, Item.IRON_ORE, Item.ALUMINIUM_ORE])
        match difficulty:
            case Difficulty.EASY:
                self.amount_needed = randrange(0, 2)*5 + 10
            case Difficulty.MEDIUM:
                self.amount_needed = randrange(0, 2)*5 + 15
            case Difficulty.HARD:
                self.amount_needed = randrange(0, 1)*10 + 15
            case Difficulty.EXPERT:
                self.amount_needed = randrange(0, 1)*15 + 15

    def advance(self, by: int = 1) -> None:
        super(QuestGatherOre, self).advance(by)
        self.progress = min(self.progress, self.amount_needed)

    def is_completed(self) -> bool:
        return self.progress == self.amount_needed

    def get_progress_status_text(self) -> str:
        return f"Gather {self.amount_needed} {self.ore_type.name.lower()}: {self.progress}/{self.amount_needed}"


if __name__ == '__main__':
    pass
