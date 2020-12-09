import imgui
import imgui.core

from arcade_imgui import ArcadeRenderer


class ArcadeImGui:
    def __init__(self, window):
        self.window = window
        # Must create or set the context before instantiating the renderer
        imgui.create_context()
        self.renderer = ArcadeRenderer(window)

    def __enter__(self):
        imgui.new_frame()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.render()

    def render(self):
        imgui.render()
        self.renderer.render(imgui.get_draw_data())