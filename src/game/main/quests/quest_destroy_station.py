

from dataclasses import dataclass

from src.game.main.enums.difficulty import Difficulty
from src.game.main.quests.quest import Quest
from src.game.main.quests.quest_type import QuestType
from src.game.main.util.rand import randrange


@dataclass
class QuestDestroyStation(Quest):
    type_ = QuestType.DESTROY_STATION

    def generate(self, difficulty: Difficulty = Difficulty.MEDIUM, seed: int = 0) -> None:
        self.type_ = QuestType.DESTROY_STATION # TODO tmp fix

    def advance(self, by: int = 1) -> None:
        super(QuestDestroyStation, self).advance(by)
        self.progress = min(self.progress, 1)

    def is_completed(self) -> bool:
        return self.progress == 1

    def get_progress_status_text(self) -> str:
        return f"Destroy enemy station: {self.progress}/1"


if __name__ == '__main__':
    pass
