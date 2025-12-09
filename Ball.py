from OpenGL.GL import *
from OpenGL.GLU import *

from Color import Color
from Paddle import Paddle


class Ball:
    def __init__(self, paddle: Paddle):
        self.radius = paddle.depth / 2.0
        self.paddle = paddle
        self.stick_to_paddle = True

        # posisi awal mengikuti paddle
        self.x = paddle.x
        self.y = paddle.y + 2 * self.radius
        self.z = self.radius + 0.05

        self.vx = 0.0
        self.vy = 0.0
        self.speed = 8.0

    def launch(self, direction: str = "up_right"):
        self.stick_to_paddle = False
        if direction == "up_right":
            self.vx = self.speed * 0.7
            self.vy = self.speed
        elif direction == "up_left":
            self.vx = -self.speed * 0.7
            self.vy = self.speed
        else:
            self.vx = 0.0
            self.vy = self.speed

    def update(self, dt: float, table_width: float, table_height: float):
        if self.stick_to_paddle:
            self.x = self.paddle.x
            self.y = self.paddle.y + 2 * self.radius
        else:
            self.x += self.vx * dt
            self.y += self.vy * dt

            # cek dinding kiri/kanan
            if self.x - self.radius <= -table_width / 2 or \
               self.x + self.radius >= table_width / 2:
                self.vx *= -1

            # cek dinding atas
            if self.y + self.radius >= table_height / 2:
                self.vy *= -1

            # tidak ada cek batas bawah — biarkan game mendeteksinya

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glColor3fv(Color.WHITE.value)
        quadric = gluNewQuadric()
        gluSphere(quadric, self.radius, 16, 16)
        glPopMatrix()
