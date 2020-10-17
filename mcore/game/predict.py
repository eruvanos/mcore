import time
from collections import deque
from typing import Union, NamedTuple, Deque

from pymunk import Vec2d


class Snapshot(NamedTuple):
    value: Union[int, Vec2d]
    time: float


class PredictedValue:
    last_update: float

    def __init__(self, value: Union[int, Vec2d] = None):
        self.position_buffer: Deque[Snapshot] = deque(maxlen=2)

        if value:
            self.set(value)

    def set(self, value: Union[int, Vec2d]):
        cur_time = time.time()
        self.position_buffer.append(Snapshot(value, cur_time))
        self.last_update = cur_time

    def get(self):
        if len(self.position_buffer) == 2:
            return self.predict()
        elif len(self.position_buffer) == 1:
            return self.position_buffer[0][0]
        elif len(self.position_buffer) == 0:
            return None

    def latest(self):
        if len(self.position_buffer) == 0:
            return None
        else:
            return self.position_buffer[-1]

    def predict(self, at_time=None):
        if at_time is None:
            at_time = time.time()

        # These are the last two positions. p1 is the latest, p0 is the
        # one immediately preceding it.
        p0, t0 = self.position_buffer[0]
        p1, t1 = self.position_buffer[1]

        if not (isinstance(p0, Vec2d) or isinstance(p0, int)):
            raise TypeError(f'Value has to be int or Vec2d, but was {type(p0)}')

        if not (isinstance(p1, Vec2d) or isinstance(p1, int)):
            raise TypeError(f'Value has to be int or Vec2d, but was {type(p1)}')

        dtt = t1 - t0
        if dtt == 0:
            return self.position_buffer[0].value

        # Calculate a PREDICTED future position, based on these two.
        velocity = (p1 - p0) / dtt

        # predicted position for next update
        predicted_position = velocity * dtt + p1

        # guess current position (on our way to the predicted)
        time_since_state_update = at_time - t1
        x = (time_since_state_update - 0) / dtt
        x = min(x, 1)
        return p1 + (predicted_position - p1) * x


if __name__ == '__main__':
    v1 = Vec2d(1, 3)
    v2 = Vec2d(2, 4)

    for range in [
        0.5,
        0.1,
        1.5,
        -0.5,
        0,
        20,
    ]:
        print('Range ', range)
        print(v1.interpolate_to(v2, range))
        print(v1 + (v2 - v1) * range)
        print()
