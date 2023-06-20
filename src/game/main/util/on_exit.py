from src.game.main.save.game_save import GameSave
from src.game.main.singletons.player_statistics import PlayerStatistics


def on_exit():
    PlayerStatistics.save()
    GameSave.save()
