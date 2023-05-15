

from dataclasses import dataclass

from src.game.main.enums.difficulty import Difficulty
from src.game.main.quests.quest import Quest
from src.game.main.quests.quest_type import QuestType
from src.game.main.util.rand import randrange


@dataclass
class QuestKillCount(Quest):
    type_ = QuestType.KILL_SUM
    kills_needed: int = 0

    def generate(self, difficulty: Difficulty = Difficulty.MEDIUM, seed: int = 0) -> None:
        match difficulty:
            case Difficulty.EASY:
                self.kills_needed = randrange(0, 3)*5 + 10
            case Difficulty.MEDIUM:
                self.kills_needed = randrange(0, 3)*5 + 15
            case Difficulty.HARD:
                self.kills_needed = randrange(0, 2)*10 + 20
            case Difficulty.EXPERT:
                self.kills_needed = randrange(0, 1)*15 + 25

    def advance(self, by: int = 1) -> None:
        super(QuestKillCount, self).advance(by)
        self.progress = min(self.progress, self.kills_needed)

    def is_completed(self) -> bool:
        return self.progress == self.kills_needed

    def get_progress_status_text(self) -> str:
        return f"Destroy {self.kills_needed} enemies: {self.progress}/{self.kills_needed}"


if __name__ == '__main__':
    pass
