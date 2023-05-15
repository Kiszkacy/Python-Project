from array import array
from typing import List, Dict, Generator

import arcade
import arcade.gl
import numpy as np

from src.game.main.enums.particle import Particle, ParticleFragmentShader
from src.game.main.events.damage_event import DamageEvent
from src.game.main.events.event import Event
from src.game.main.events.event_observer import Observer
from src.game.main.interfaces.processable import Processable
from src.game.main.particles.burst import Burst
from src.game.main.singletons.config import Config
from src.game.main.singletons.event_register import EventRegister
from src.game.main.util.path_loader import get_absolute_resource_path


class ParticlesHandler(Observer, Processable):

    def __init__(self, ctx: arcade.ArcadeContext, camera: arcade.Camera) -> None:
        self.gl_ctx: arcade.ArcadeContext = ctx
        self.camera: arcade.Camera = camera
        self.particles: Dict[Particle, arcade.gl.Program] = {}
        self.active: List[Burst] = []
        self.time: float = 0.0

    def setup(self) -> None:
        # load all shaders from resources depending on Particle enum
        path: str = get_absolute_resource_path("\\particle_shaders\\")
        for p in Particle:
            vertex_path: str = f"{path}vertex\\{p.name.lower()}.glsl"
            fragment_path: str = f"{path}fragment\\{ParticleFragmentShader[p]}.glsl"
            self.particles[p] = self.gl_ctx.load_program(vertex_shader=vertex_path, fragment_shader=fragment_path)
        # add itself as an observer
        EventRegister.add_observer(self)

    def notify(self, about: Event) -> None:
        type_: Particle = Particle.DAMAGE
        at: arcade.Point = (0, 0)
        found: bool = False
        if isinstance(about, DamageEvent):
            type_ = Particle.DAMAGE
            event: DamageEvent = about
            at = event.damaged.position
            # print(event.damaged)
            found = True

        # if found: self.create_burst(
        #     (at[0]-self.camera.position[0] - Config.Settings.get("SCREEN_WIDTH") / 2.0,
        #      at[1]-self.camera.position[1] - Config.Settings.get("SCREEN_HEIGHT") / 2.0), type_)
        if found: self.create_burst(at, type_)

    def create_burst(self, at: arcade.Point, type_: Particle) -> None:
        """code mostly from arcade docs examples"""
        def _generate_data(x: float, y: float, type_: Particle):
            for _ in range(200): # TODO hardcoded particle count
                angle: float = np.random.uniform(0, 2 * np.pi)
                speed: float = abs(np.random.normal(0, 1)) * 0.3
                dx: float = np.sin(angle) * speed
                dy: float = np.cos(angle) * speed
                red: float = np.random.uniform(0.5, 1.0)
                green: float = np.random.uniform(0, red)
                blue: float = 0
                fade_rate: float = np.random.uniform(1 / 1.2, 1 / 1.2) # TODO hardcoded max particle duration

                yield x
                yield y
                yield dx
                yield dy
                yield red
                yield green
                yield blue
                yield fade_rate

        # offset position to opengl system [e.g. for x: 0 -> SCREEN_WIDTH | in opengl: -1.0 -> 1.0]
        x_off: float = at[0] / Config.Settings.get("SCREEN_WIDTH") * 2.0 - 1.0
        y_off: float = at[1] / Config.Settings.get("SCREEN_HEIGHT") * 2.0 - 1.0

        # create initial data
        # print("AT", at)
        # print("AT2", x_off, y_off)
        data = _generate_data(x_off, y_off, type_)

        # create buffer with given data
        buffer: arcade.gl.Buffer = self.gl_ctx.buffer(data=array("f", data))

        # buffer description that says how the buffer data is formatted
        buffer_description: arcade.gl.BufferDescription = arcade.gl.BufferDescription(buffer, "2f 2f 3f f",
                                                                                      ["in_pos",
                                                                                       "in_vel",
                                                                                       "in_color",
                                                                                       "in_fade_rate"])

        # create vao - vertex attribute object
        vao: arcade.gl.Geometry = self.gl_ctx.geometry([buffer_description])

        self.active.append(Burst(buffer, vao, self.time, type_))

    def process(self, delta: float) -> None:
        self.time += delta

        # remove all old bursts
        copied: List[Burst] = self.active.copy()
        for burst in copied:
            if self.time - burst.start > 1.2: # TODO hardcoded max particle duration
                self.active.remove(burst)

    def draw(self) -> None:
        # set the particle size
        self.gl_ctx.point_size = 3.0 # TODO add pixel ratio here from window

        for burst in self.active:
            # set uniform data
            program: arcade.gl.Program = self.particles[burst.particle_type]
            program["time"] = self.time - burst.start
            # offset camera position to opengl
            x_off: float = (self.camera.position[0]+Config.Settings.get("SCREEN_WIDTH")*0.5) / Config.Settings.get("SCREEN_WIDTH") * 2.0 - 1.0
            y_off: float = (self.camera.position[1]+Config.Settings.get("SCREEN_HEIGHT")*0.5) / Config.Settings.get("SCREEN_HEIGHT") * 2.0 - 1.0
            program["camera_pos_offset"] = (x_off, y_off)

            # print("camera", (x_off, y_off))
            # render burst
            burst.vao.render(self.particles[burst.particle_type], mode=self.gl_ctx.POINTS)


if __name__ == '__main__':
    pass
