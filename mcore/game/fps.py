import arcade


class FPSDisplay:
    """Display of a window's framerate.
    This is a convenience class to aid in profiling and debugging.  Typical
    usage is to create an `FPSDisplay` for each window, and draw the display
    at the end of the windows' :py:meth:`~pyglet.window.Window.on_draw` event handler::
        window = pyglet.window.Window()
        fps_display = FPSDisplay(window)
        @window.event
        def on_draw():
            # ... perform ordinary window drawing operations ...
            fps_display.draw()
    The style and position of the display can be modified via the :py:func:`~pyglet.text.Label`
    attribute.  Different text can be substituted by overriding the
    `set_fps` method.  The display can be set to update more or less often
    by setting the `update_period` attribute. Note: setting the `update_period`
    to a value smaller than your Window refresh rate will cause inaccurate readings.
    :Ivariables:
        `label` : Label
            The text label displaying the framerate.
    """

    #: Time in seconds between updates.
    #:
    #: :type: float
    update_period = 1.0

    def __init__(self, window):
        from time import time
        # self.label = Text('', x=10, y=10,
        #                    font_size=24, bold=True,
        #                    color=(127, 127, 127, 127))
        self.label = ' '

        self.window = window
        self._window_flip = window.flip
        window.flip = self._hook_flip

        self.time = 0.0
        self.last_time = time()
        self.count = 0

    def update(self):
        """Records a new data point at the current time.  This method
        is called automatically when the window buffer is flipped.
        """
        from time import time
        t = time()
        self.count += 1
        self.time += t - self.last_time
        self.last_time = t

        if self.time >= self.update_period:
            self.set_fps(self.count / self.time)
            self.time %= self.update_period
            self.count = 0

    def set_fps(self, fps):
        """Set the label text for the given FPS estimation.
        Called by `update` every `update_period` seconds.
        :Parameters:
            `fps` : float
                Estimated framerate of the window.
        """
        self.label = '%.0f' % fps

    def draw(self):
        """Draw the label.
        The OpenGL state is assumed to be at default values, except
        that the MODELVIEW and PROJECTION matrices are ignored.  At
        the return of this method the matrix mode will be MODELVIEW.
        """
        arcade.draw_text(
            self.label,
            start_x=10, start_y=10,
            color=(127, 127, 127, 127),
            font_size=24
        )

    def _hook_flip(self):
        self.update()
        self._window_flip()