from OpenGL.GL import *
from OpenGL.GLU import *

from Color import Color
from Paddle import Paddle


# ========================
# Ball
# ========================
class Ball:
    def __init__(self, paddle: Paddle):
        self.radius = paddle.depth / 2.0
        self.paddle = paddle
        self.stick_to_paddle = True  # masih nempel paddle
        self.x = paddle.x
        self.y = paddle.y + 2 * self.radius
        self.z = self.radius + 0.05
        self.vx = 0.0
        self.vy = 0.0
        self.speed = 8.0  # kecepatan bola

    def launch(self, direction: str = "up_right"):
        """ Lepasin bola dari paddle ke arah tertentu """
        self.stick_to_paddle = False
        if direction == "up_right":
            self.vx = self.speed * 0.7   # ke kanan
            self.vy = self.speed * 1.0   # ke atas
        elif direction == "up_left":
            self.vx = -self.speed * 0.7
            self.vy = self.speed * 1.0
        else:  # default lurus atas
            self.vx = 0.0
            self.vy = self.speed

    def update(self, dt: float, table_width: float, table_height: float):
        if self.stick_to_paddle:
            self.x = self.paddle.x
            self.y = self.paddle.y + 2 * self.radius
        else:
            self.x += self.vx * dt
            self.y += self.vy * dt

            # cek tabrakan dengan batas kiri/kanan
            if self.x - self.radius <= -table_width / 2 or self.x + self.radius >= table_width / 2:
                self.vx *= -1  # mantul horizontal

            # cek tabrakan dengan batas atas/bawah
            if self.y + self.radius >= table_height / 2 or self.y - self.radius <= -table_height / 2:
                self.vy *= -1  # mantul vertical

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glColor3fv(Color.WHITE.value)
        quadric = gluNewQuadric()
        gluSphere(quadric, self.radius, 16, 16)
        glPopMatrix()

