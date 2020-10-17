from typing import List

from arcade import Sprite


class Transition:
    def __init__(self, duration: float, start, end, name, delay):
        self.start = start
        self.end = end
        self.name = name

        self.duration = duration  # * 1000
        self.elapsed = -delay

    def update(self, sprite, dt):
        self.elapsed += dt
        if self.elapsed > 0:
            progress = self.elapsed / self.duration
            setattr(sprite, self.name, (self.start + (self.end - self.start) * progress))

    @property
    def finished(self):
        return self.elapsed / self.duration >= 1


class Effect:
    def __init__(self, sprite: Sprite):
        self.sprite = sprite
        self.transitions: List[Transition] = []

    def add_transition(self, duration: float, start, end, property: str, delay=0):
        self.transitions.append(Transition(duration, start, end, property, delay))

    def draw(self):
        self.sprite.draw()

    def update(self, dt):
        for t in self.transitions:
            t.update(self.sprite, dt)

        for t in self.transitions[:]:
            if t.finished:
                self.transitions.remove(t)

    @property
    def transition_left(self):
        return len(self.transitions) == 0
