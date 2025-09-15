from OpenGL.GL import *

from Color import Color
from draw_cube import draw_cube


# ========================
# Brick
# ========================
class Brick:
    WIDTH = 0.8
    HEIGHT = 0.4
    DEPTH = 0.3
    COLOR = Color.MAROON.value

    def __init__(
            self, pos_x, pos_y,
            width=WIDTH,
            height=HEIGHT,
            depth=DEPTH,
            color=COLOR
    ):
        self.x = pos_x
        self.y = pos_y
        self.width = width
        self.height = height
        self.depth = depth
        self.color = color

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.depth / 2.0 + 0.05)
        draw_cube(self.width, self.height, self.depth, self.color)
        glPopMatrix()

