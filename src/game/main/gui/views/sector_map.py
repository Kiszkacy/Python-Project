import arcade
from arcade import gui

from src.game.main.gui.views.fading_view import FadingView
from src.game.main.gui.views.game_view import GameView
from src.game.main.gui.views.view import View
from src.game.main.sectors import biomes
from src.game.main.sectors.sector import Sector
from src.game.main.sectors.sector_master import SectorMaster, Node
from src.game.main.singletons.game_save import GameSave
from src.game.main.singletons.input_handler import InputHandler


class SectorMap(FadingView):
    game: FadingView = None

    def __init__(self, window: arcade.Window) -> None:
        super(SectorMap, self).__init__(window)
        self.manager: gui.UIManager = arcade.gui.UIManager()
        self.layout: gui.UIBoxLayout = None

        GameSave.innit()
        GameSave.save()
        self.sector_master = SectorMaster(GameSave.stats["seed"])
        self.sector_master.initialize()

        if SectorMap.game is None:
            SectorMap.game = GameView(self.window, self.sector_master.current_sector)
        self.sector_map = self.sector_master.get_sector_map()
        self.inspected_sector_node: Node = None
        self.sector_info_text: gui.UITextArea = None

    def setup(self) -> None:

        self.manager.enable()
        self.layout = gui.UIBoxLayout()

        title = gui.UILabel(text="SECTOR MAP", text_color=arcade.color.BLACK, font_size=50)
        self.layout.add(gui.UIAnchorWidget(child=title, anchor_y="top", align_y=-100))
        map_box = gui.UIBoxLayout(size_hint_max=400)
        self.layout.add(map_box)
        self.sector_info_text = gui.UITextArea(text="Select sector to see information", font_size=12, width=400, height=100)

        for node, coordinates in self.sector_map.items():
            button_colour = biomes.get_biome_color_theme(node.sector.type)
            button = gui.UITextureButton(texture=arcade.make_circle_texture(30, button_colour))
            button.on_click = self.get_sector_info_fun(node)
            map_box.add(gui.UIAnchorWidget(child=button, align_x=coordinates.x * 30, align_y=coordinates.y * 30 + 80))

        self.layout.add(gui.UITextArea(text="Sector Info", font_size=24))
        vbox = gui.UIBoxLayout(vertical=False)
        self.layout.add(vbox)
        start_button = gui.UIFlatButton(text="Start")
        start_button.on_click = self.on_click_start_button

        vbox.add(self.sector_info_text)
        vbox.add(gui.UIAnchorWidget(child=start_button, anchor_y="top", anchor_x="right"))

        # NOTE: I think this magical code automatically centers whole ui ?
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.layout)
        )

    def get_sector_info_fun(self, node: Node):
        def on_click(event: gui.events.UIEvent) -> None:
            self.inspected_sector_node = node
            self.sector_info_text.text = f"Sector type: {self.format_text(node.sector.type.name)}\n" \
                                         f"Sector size: {self.format_text(node.sector.size.name)}\n" \
                                         f"Sector difficulty: {self.format_text(node.sector.difficulty.name)}"
        return on_click

    def format_text(self, text: str):
        return text.lower().capitalize().replace("_", " ")

    def on_click_start_button(self, event: gui.events.UIEvent) -> None:
        self.sector_master.current_sector_node = self.inspected_sector_node
        self.game.sector = self.inspected_sector_node.sector
        # SectorMap.game.setup()
        # self.window.show_view(self.game)
        self.switch_view(self.game)

    def on_update(self, delta_time: float) -> None:
        super(SectorMap, self).on_update(delta_time)

    def on_draw(self) -> None:
        self.clear()
        self.manager.draw()
        super(SectorMap, self).on_draw()  # draw last so fade-in fade-out works


if __name__ == '__main__':
    pass
