from typing import Optional, List

import arcade
from arcade import Sound

DEFAULT_MUSIC_VOLUME = 0.05
DEFAULT_EFFECT_VOLUME = 0.3


class SoundPlayer:
    def __init__(self,
                 base_music_volume=DEFAULT_MUSIC_VOLUME,
                 base_effect_volume=DEFAULT_EFFECT_VOLUME
                 ):
        self.base_effect_volume = base_effect_volume
        self.base_music_volume = base_music_volume

        self._current_music: Optional[Sound] = None
        self._current_effects: List[Sound] = []

        self._music_playing = False
        self._loop_playing = False

        self._music_volume = 1.0
        self._effect_volume = 1.0

        self._mute: int = 1

    def play_music(self, sound: Sound, loop=True):
        if self._music_playing:
            self._current_music.stop()

        self._current_music = sound
        self._current_music.play(self.music_level)
        self._music_playing = True

        if loop and not self._loop_playing:
            arcade.schedule(self.__loop_play, self._current_music.get_length())
            self._loop_playing = True

    def __loop_play(self, *args):
        self.play_music(self._current_music, loop=False)

    def stop_music(self):
        arcade.unschedule(self.__loop_play)
        self._current_music.stop()
        self._music_playing = False
        self._loop_playing = False

    def play_effect(self, sound: Sound):
        # TODO add effect to effect list, also remove them after play time
        # self._current_effects.append(sound)
        sound.play(self.effect_level)

    def mute(self):
        self._mute = 0

        self._current_music.set_volume(self.music_level)
        for effect in self._current_effects:
            effect.set_volume(self.effect_level)

    def unmute(self):
        self._mute = 1

        self._current_music.set_volume(self.music_level)
        for effect in self._current_effects:
            effect.set_volume(self.effect_level)

    @property
    def music_volume(self) -> float:
        return self._music_volume

    @music_volume.setter
    def music_volume(self, value: float):
        self._music_volume = value

        if self._current_music:
            self._current_music.set_volume(self.music_level)

    @property
    def effect_level(self):
        return self._mute * self.base_effect_volume * self._effect_volume

    @property
    def music_level(self):
        return self._mute * self.base_music_volume * self._music_volume

    @property
    def effect_volume(self) -> float:
        return self._effect_volume

    @effect_volume.setter
    def effect_volume(self, value: float):
        self._effect_volume = value

        for effect in self._current_effects:
            effect.set_volume(self.effect_level)