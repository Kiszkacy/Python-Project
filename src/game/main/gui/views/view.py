from __future__ import annotations
from abc import ABC, abstractmethod

import arcade


class View(arcade.View, ABC):
    """Wrapper class for arcade.View one."""
    def __init__(self, window: arcade.Window) -> None:
        super(View, self).__init__(window)

    @abstractmethod
    def setup(self) -> None:
        pass

    def switch_view(self, to: View) -> None:
        to.setup()
        self.window.show_view(to)


if __name__ == '__main__':
    pass
