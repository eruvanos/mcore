"""
Implementation for animations in arcade.

animation = Animation(
    center_x=event.pos.x,
    center_y=event.pos.y,
)
animation.add_frame(150, './resources/effects/explosion1.png', 0.3)
animation.add_frame(150, './resources/effects/explosion2.png', 0.6)
animation.add_frame(150, './resources/effects/explosion3.png', 0.9)
self.animations.append(animation)

class GameView(arcade.View):
    def __init__(self, ui_manager: UIManager):
        super().__init__()
        self.animations = SpriteList()

    def on_update(self, delta_time: float):
        self.animations.update_animation(delta_time)

    def on_draw(self):
        arcade.start_render()
        self.animations.draw()
"""

import dataclasses
from pathlib import Path
from typing import Union, List

from arcade import load_texture, Sprite, Texture


@dataclasses.dataclass
class AnimationFrame:
    """
    Used in animated sprites.
    """
    duration: int
    texture: Texture
    scale: float


class Animation(Sprite):
    def __init__(self,
                 scale: float = 1,
                 center_x: float = 0,
                 center_y: float = 0,
                 ):
        super().__init__(
            scale=scale,
            center_x=center_x,
            center_y=center_y
        )

        self.cur_frame_idx = 0
        self.frames: List[AnimationFrame] = []
        self.time_counter = 0.0

        self.duration_ms = 0
        self.total_time_ms = 0

    def add_frame(self, duration: int, file: Union[str, Path], scale=1.0):
        """
        :param file: Union[str, Path] Frame image to add
        :type duration: int Duration in ms
        """
        frame_texture = load_texture(file, hit_box_algorithm='None')

        if len(self.frames) == 0:
            self.texture = frame_texture

        self.duration_ms += duration
        self.frames.append(
            AnimationFrame(duration, frame_texture, scale)
        )

    def update_animation(self, delta_time: float = 1 / 60):
        """
        Logic for selecting the proper texture to use.
        :type delta_time: float in seconds
        """
        self.total_time_ms += delta_time * 1000
        if self.total_time_ms > self.duration_ms:
            self.kill()

        # Legacy update code
        self.time_counter += delta_time
        while self.time_counter > self.frames[self.cur_frame_idx].duration / 1000.0:
            self.time_counter -= self.frames[self.cur_frame_idx].duration / 1000.0
            self.cur_frame_idx += 1
            if self.cur_frame_idx >= len(self.frames):
                self.cur_frame_idx = 0
            # source = self.frames[self.cur_frame].texture.image.source
            cur_frame = self.frames[self.cur_frame_idx]
            # print(f"Advance to frame {self.cur_frame_idx}: {cur_frame.texture.name}")
            self.texture = cur_frame.texture
            self.scale = cur_frame.scale
