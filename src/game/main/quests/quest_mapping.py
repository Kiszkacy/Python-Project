
from typing import Type, List, Dict

from src.game.main.quests.quest import Quest
from src.game.main.quests.quest_gather_ore import QuestGatherOre
from src.game.main.quests.quest_kill_count import QuestKillCount
from src.game.main.quests.quest_type import QuestType

MainQuests: List[QuestType] = [QuestType.KILL_SUM, QuestType.GATHER_ORE]

SideQuests: List[QuestType] = [QuestType.KILL_SUM, QuestType.GATHER_ORE]

# pseudo-fake class-dict something
QuestConstructor: Dict[QuestType, Type[Quest]] = {
    QuestType.KILL_SUM: QuestKillCount,
    QuestType.GATHER_ORE: QuestGatherOre,
}


if __name__ == '__main__':
    pass
