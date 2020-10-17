from contextlib import contextmanager

import arcade
from arcade import Sprite, Window


class MarginCamera:
    def __init__(self, window: Window):
        self.window = window
        if window is None:
            raise Exception('Window required')

        # How many pixels to keep as a minimum margin between the character
        # and the edge of the screen.
        self.left_viewport_margin = 400
        self.right_viewport_margin = 400
        self.bottom_viewport_margin = 100
        self.top_viewport_margin = 300

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

    def update(self, player: Sprite):
        changed = False

        # Scroll left
        left_boundary = self.view_left + self.left_viewport_margin
        if player.left < left_boundary:
            self.view_left -= left_boundary - player.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + self.window.width - self.right_viewport_margin
        if player.right > right_boundary:
            self.view_left += player.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + self.window.height - self.top_viewport_margin
        if player.top > top_boundary:
            self.view_bottom += player.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + self.bottom_viewport_margin
        if player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - player.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                self.window.width + self.view_left,
                                self.view_bottom,
                                self.window.height + self.view_bottom)


class ZoomCamera:
    def __init__(self, window: Window):
        if window is None:
            raise Exception('Window required')

        self._window = window
        self._zoom = 1

    def get_pos(self, x: int, y: int):
        """
        Calculates in game position of mouse
        """
        w_width, w_height = self._window.get_size()
        left, right, bottom, top = self._window.get_viewport()

        x = left + (right - left) * x / w_width
        y = bottom + (top - bottom) * y / w_height

        return x, y

    def on_scroll(self, direction: int):
        if direction > 0:
            self._zoom = max(self._zoom - 0.1, 0.5)
        elif direction < 0:
            self._zoom = min(self._zoom + 0.1, 2)

    def update(self, player: Sprite):
        width, height = self._window.get_size()

        c_x = player.center_x
        c_y = player.center_y

        width = width * self._zoom
        height = height * self._zoom

        self._window.set_viewport(
            left=c_x - width // 2,
            right=c_x + width // 2,
            bottom=c_y - height // 2,
            top=c_y + height // 2,
        )


class FreeCamera:
    def __init__(self, window: Window = None):
        if window is None:
            window = arcade.get_window()

        self._window = window
        self._zoom = 1

        self.center = window.width // 2, window.height // 2

    def get_pos(self, x: int, y: int):
        """
        Calculates in game position of mouse
        """
        w_width, w_height = self._window.get_size()
        left, right, bottom, top = self._window.get_viewport()

        x = left + (right - left) * x / w_width
        y = bottom + (top - bottom) * y / w_height

        return x, y

    def on_scroll(self, direction: int):
        if direction > 0:
            self._zoom = max(self._zoom - 0.1, 0.5)
        elif direction < 0:
            self._zoom = min(self._zoom + 0.1, 2)

    def to_world_coords(self, x: float, y: float):
        return x + self.viewport()[0], y + self.viewport()[2]

    @contextmanager
    def view(self):
        old_viewport = self._window.get_viewport()
        self._window.set_viewport(*self.viewport())
        yield
        self._window.set_viewport(*old_viewport)

    def viewport(self):
        width, height = self._window.get_size()

        width = width * self._zoom
        height = height * self._zoom

        c_x, c_y = self.center

        return c_x - width // 2, c_x + width // 2, c_y - height // 2, c_y + height // 2

    def move(self, dx, dy):
        self.center = self.center[0] + dx, self.center[1] + dy