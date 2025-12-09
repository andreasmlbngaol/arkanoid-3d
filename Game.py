import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Ball import Ball
from Brick import Brick
from Paddle import Paddle
from Table import Table
from MouseEvent import MouseEvent

class Game:
    FRAME_RATE = 240
    PADDLE_SPEED = 12
    DISPLAY_SIZE = (800, 600)

    def __init__(self):
        pygame.init()
        pygame.display.set_mode(self.DISPLAY_SIZE, DOUBLEBUF | OPENGL)

        # depth test aktif
        glEnable(GL_DEPTH_TEST)

        # kamera state
        self.display = self.DISPLAY_SIZE
        self.camera_zoom = -15
        self.camera_rot_x = -70.0
        self.camera_rot_y = 0.0
        self.camera_rot_z = 0.0
        self.dragging = False
        self.last_mouse_pos: tuple[int, int] = (0, 0)

        # objek game
        self.table = Table()
        self.paddle = Paddle()
        self.bricks = self._create_bricks(5, 7)
        self.ball = Ball(self.paddle)

    def _create_bricks(self, rows: int, cols: int, spacing_x = 0.1, spacing_y = 0.1):
        bricks: list[Brick | None] = []
        brick_width = (self.table.width - (cols - 1) * spacing_x) / cols
        brick_height = (self.table.height * (30 / 100) - (rows - 1) * spacing_y) / rows
        start_x, start_y = (-self.table.width + brick_width) / 2, (self.table.height / 2  - (brick_height * rows) - (spacing_y * (rows - 1)))
        for row in range(rows):
            for col in range(cols):
                pos_x = start_x + col * (brick_width + spacing_x)
                pos_y = start_y + spacing_y + row * (brick_height + spacing_y)
                bricks.append(Brick(pos_x, pos_y, width=brick_width, height=brick_height))
        return bricks

    def handle_input(self):
        keys = pygame.key.get_pressed()
        movement = (self.PADDLE_SPEED / self.FRAME_RATE)
        bound = self.table.width / 2
        unknown = self.paddle.width / 2.0 + 0.05
        if keys[K_LEFT]:
            if self.paddle.x - movement - unknown >= -bound:
                self.paddle.x -= movement
            else:
                self.paddle.x = -bound + unknown
        if keys[K_RIGHT]:
            if self.paddle.x + movement + unknown <= bound:
                self.paddle.x += movement
            else:
                self.paddle.x = bound - unknown

        if keys[K_SPACE] and self.ball.stick_to_paddle:
            self.ball.launch("up_right")

    def handle_mouse(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == MouseEvent.RIGHT_CLICK:  # klik kanan untuk rotate
                self.dragging = True
                pos: tuple[int, int] = event.pos
                self.last_mouse_pos = pos
            elif event.button == MouseEvent.WHEEL_UP:  # scroll up (zoom in)
                self.camera_zoom += 2.0
            elif event.button == MouseEvent.WHEEL_DOWN:  # scroll down (zoom out)
                self.camera_zoom -= 2.0

        elif event.type == MOUSEBUTTONUP and event.button == MouseEvent.RIGHT_CLICK:
            self.dragging = False

        elif event.type == MOUSEMOTION and self.dragging:
            dx = event.pos[0] - self.last_mouse_pos[0]
            dy = event.pos[1] - self.last_mouse_pos[1]
            self.camera_rot_x += dy * 0.5
            self.camera_rot_y += dx * 0.5
            self.last_mouse_pos = event.pos

    def _check_paddle_collision(self):
        # batas (bounding box) bola
        ball_left = self.ball.x - self.ball.radius
        ball_right = self.ball.x + self.ball.radius
        ball_bottom = self.ball.y - self.ball.radius

        # batas (bounding box) paddle
        paddle_left = self.paddle.x - self.paddle.width / 2
        paddle_right = self.paddle.x + self.paddle.width / 2
        paddle_top = self.paddle.y + self.paddle.height / 2
        paddle_bottom = self.paddle.y - self.paddle.height / 2

        # cek interseksi
        # Apakah bola ada dalam rentang horizontal paddle?
        collision_x = ball_right >= paddle_left and ball_left <= paddle_right
        # Apakah bola ada dalam rentang vertikal paddle?
        collision_y = ball_bottom <= paddle_top and self.ball.y >= paddle_bottom

        if collision_x and collision_y:
            # Pastikan bola bergerak ke bawah saat menabrak (supaya tidak nyangkut)
            if self.ball.vy < 0:
                self.ball.vy *= -1  # Pantulkan ke atas

                # --- Efek Sudut Pantulan (English Effect) ---
                # Hitung jarak titik tabrakan dari tengah paddle (-1.0 s/d 1.0)
                hit_pos = (self.ball.x - self.paddle.x) / (self.paddle.width / 2)

                # Ubah kecepatan horizontal (vx) berdasarkan posisi kena
                # Kena tengah = 0, Kena pinggir = miring tajam
                self.ball.vx = hit_pos * self.ball.speed * 0.8

                # Dorong bola sedikit ke atas supaya tidak terjebak di dalam paddle
                self.ball.y = paddle_top + self.ball.radius + 0.01

    def _check_brick_collision(self):
        # Loop semua brick untuk cek tabrakan
        for i, brick in enumerate(self.bricks):
            if brick is None:
                continue  # Brick sudah hancur, skip

            # 1. Hitung batas bola
            ball_left = self.ball.x - self.ball.radius
            ball_right = self.ball.x + self.ball.radius
            ball_top = self.ball.y + self.ball.radius
            ball_bottom = self.ball.y - self.ball.radius

            # 2. Hitung batas brick
            brick_left = brick.x - brick.width / 2
            brick_right = brick.x + brick.width / 2
            brick_top = brick.y + brick.height / 2
            brick_bottom = brick.y - brick.height / 2

            # 3. Cek Interseksi AABB
            if (ball_right >= brick_left and ball_left <= brick_right and
                    ball_bottom <= brick_top and ball_top >= brick_bottom):

                # --- HITUNG SISI TABRAKAN (RESOLUSI) ---
                # Hitung seberapa dalam bola masuk ke brick dari tiap sisi
                overlap_left = ball_right - brick_left
                overlap_right = brick_right - ball_left
                overlap_top = brick_top - ball_bottom
                overlap_bottom = ball_top - brick_bottom

                # Cari overlap terkecil untuk menentukan sisi tabrakan
                min_overlap_x = min(overlap_left, overlap_right)
                min_overlap_y = min(overlap_top, overlap_bottom)

                # Jika overlap horizontal lebih kecil, berarti kena samping
                if min_overlap_x < min_overlap_y:
                    self.ball.vx *= -1
                    # Koreksi posisi bola agar tidak nempel
                    if overlap_left < overlap_right:
                        self.ball.x = brick_left - self.ball.radius - 0.01
                    else:
                        self.ball.x = brick_right + self.ball.radius + 0.01
                else:
                    # Kena atas/bawah
                    self.ball.vy *= -1
                    # Koreksi posisi bola
                    if overlap_bottom < overlap_top:
                        self.ball.y = brick_bottom - self.ball.radius - 0.01
                    else:
                        self.ball.y = brick_top + self.ball.radius + 0.01

                # 4. Hancurkan Brick
                self.bricks[i] = None

                # Break agar tidak menabrak 2 brick sekaligus dalam 1 frame (opsional tapi disarankan)
                break

    def setup_camera(self):
        # Reset dan pasang kamera tiap frame
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(40, (self.display[0] / self.display[1]), 0.1, 50.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, self.camera_zoom)
        glRotatef(self.camera_rot_x, 1, 0, 0)
        glRotatef(self.camera_rot_y, 0, 1, 0)
        glRotatef(self.camera_rot_z, 0, 0, 1)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                self.handle_mouse(event)

            self.handle_input()
            dt = clock.get_time() / 1000.0  # detik
            self.ball.update(dt, self.table.width, self.table.height)

            self._check_paddle_collision()
            self._check_brick_collision()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.setup_camera()

            # gambar objek
            self.table.draw()
            self.paddle.draw()
            self.ball.draw()
            for brick in self.bricks:
                if brick is None:
                    continue
                brick.draw()

            pygame.display.flip()
            clock.tick(self.FRAME_RATE)

        pygame.quit()
