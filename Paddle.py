from OpenGL.GL import *

from Color import Color
from draw_cube import draw_cube


class Paddle:
    WIDTH = 2.0
    HEIGHT = 0.4
    DEPTH = 0.4
    COLOR = Color.GREEN.value

    def __init__(self, pos_x=0, pos_y=-4, width=WIDTH, height=HEIGHT, depth=DEPTH):
        self.x = pos_x
        self.y = pos_y
        self.width = width
        self.height = height
        self.depth = depth

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.depth / 2.0 + 0.05)
        draw_cube(self.width, self.height, self.depth, self.COLOR)  # biru
        glPopMatrix()
