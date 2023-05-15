
from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.game.main.enums.difficulty import Difficulty
from src.game.main.quests.quest_type import QuestType


@dataclass
class Quest(ABC):
    type_: QuestType = QuestType.KILL_SUM # TODO make "ERROR TYPE" default one
    progress: int = 0

    @abstractmethod
    def generate(self, difficulty: Difficulty = Difficulty.MEDIUM, seed: int = 0) -> None:
        # r.seed(seed) # NOTE: this is not needed, because Sector calls random.seed()
        pass

    def advance(self, by: int = 1) -> None:
        self.progress += by

    @abstractmethod
    def is_completed(self) -> bool:
        pass

    @abstractmethod
    def get_progress_status_text(self) -> str:
        return "NOT IMPLEMENTED"


if __name__ == '__main__':
    pass
