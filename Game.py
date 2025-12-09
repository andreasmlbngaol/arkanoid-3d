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

        # Aktifkan depth test agar objek 3D dirender dengan urutan yang benar
        glEnable(GL_DEPTH_TEST)

        # Set kamera default
        self.display = self.DISPLAY_SIZE
        self.camera_zoom = -15
        self.camera_rot_x = -70.0
        self.camera_rot_y = 0.0
        self.camera_rot_z = 0.0
        self.dragging = False
        self.last_mouse_pos: tuple[int, int] = (0, 0)

        # Status permainan
        self.lives = 3
        self.game_over = False
        self.game_won = False

        # Objek utama game
        self.table = Table()
        self.paddle = Paddle()
        self.bricks = self._create_bricks(5, 7)  # jumlah baris & kolom brick
        self.ball = Ball(self.paddle)

        # Caption awal
        pygame.display.set_caption(f"Arkanoid 3D | Lives: {self.lives}")

    def _create_bricks(self, rows: int, cols: int, spacing_x=0.1, spacing_y=0.1):
        """Membuat susunan brick dalam grid di area atas meja"""
        bricks: list[Brick | None] = []
        brick_width = (self.table.width - (cols - 1) * spacing_x) / cols
        brick_height = (self.table.height * (30 / 100) - (rows - 1) * spacing_y) / rows

        start_x = (-self.table.width + brick_width) / 2
        # Mulai dari sisi atas area permainan
        start_y = (self.table.height / 2 - (brick_height * rows) - (spacing_y * (rows - 1)))

        for row in range(rows):
            for col in range(cols):
                pos_x = start_x + col * (brick_width + spacing_x)
                pos_y = start_y + spacing_y + row * (brick_height + spacing_y)
                bricks.append(Brick(pos_x, pos_y, width=brick_width, height=brick_height))
        return bricks

    def handle_input(self):
        """Input keyboard untuk gerakan paddle"""
        keys = pygame.key.get_pressed()
        movement = (self.PADDLE_SPEED / self.FRAME_RATE)
        bound = self.table.width / 2
        unknown = self.paddle.width / 2.0 + 0.05

        # Gerak ke kiri
        if keys[K_LEFT]:
            if self.paddle.x - movement - unknown >= -bound:
                self.paddle.x -= movement
            else:
                self.paddle.x = -bound + unknown

        # Gerak ke kanan
        if keys[K_RIGHT]:
            if self.paddle.x + movement + unknown <= bound:
                self.paddle.x += movement
            else:
                self.paddle.x = bound - unknown

        # Launch bola dari paddle
        if keys[K_SPACE] and self.ball.stick_to_paddle:
            self.ball.launch("up_right")

    def handle_mouse(self, event):
        """Input mouse untuk rotasi kamera & zoom"""
        if event.type == MOUSEBUTTONDOWN:
            if event.button == MouseEvent.RIGHT_CLICK:  # mulai drag kamera
                self.dragging = True
                self.last_mouse_pos = event.pos
            elif event.button == MouseEvent.WHEEL_UP:   # zoom in
                self.camera_zoom += 2.0
            elif event.button == MouseEvent.WHEEL_DOWN: # zoom out
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
        """Pantulan bola ke paddle, termasuk efek samping (English effect)"""
        # Area bola
        ball_left = self.ball.x - self.ball.radius
        ball_right = self.ball.x + self.ball.radius
        ball_bottom = self.ball.y - self.ball.radius

        # Area paddle
        paddle_left = self.paddle.x - self.paddle.width / 2
        paddle_right = self.paddle.x + self.paddle.width / 2
        paddle_top = self.paddle.y + self.paddle.height / 2
        paddle_bottom = self.paddle.y - self.paddle.height / 2

        # Cek overlap sederhana
        collision_x = ball_right >= paddle_left and ball_left <= paddle_right
        collision_y = ball_bottom <= paddle_top and self.ball.y >= paddle_bottom

        if collision_x and collision_y:
            # Hanya pantul jika bola sedang turun
            if self.ball.vy < 0:
                self.ball.vy *= -1

                # Hit ratio dari tengah paddle → menentukan arah pantulan
                hit_pos = (self.ball.x - self.paddle.x) / (self.paddle.width / 2)
                self.ball.vx = hit_pos * self.ball.speed * 0.8

                # Dorong bola sedikit agar tidak menempel paddle
                self.ball.y = paddle_top + self.ball.radius + 0.01

    def _check_brick_collision(self):
        """Cek tabrakan bola dengan brick, termasuk penentuan sisi mana yang kena"""
        for i, brick in enumerate(self.bricks):
            if brick is None:
                continue

            # Boundary bola
            ball_left = self.ball.x - self.ball.radius
            ball_right = self.ball.x + self.ball.radius
            ball_top = self.ball.y + self.ball.radius
            ball_bottom = self.ball.y - self.ball.radius

            # Boundary brick
            brick_left = brick.x - brick.width / 2
            brick_right = brick.x + brick.width / 2
            brick_top = brick.y + brick.height / 2
            brick_bottom = brick.y - brick.height / 2

            # Check AABB overlap
            if (ball_right >= brick_left and ball_left <= brick_right and
                    ball_bottom <= brick_top and ball_top >= brick_bottom):

                # Hitbox overlap untuk menentukan sisi pantulan
                overlap_left = ball_right - brick_left
                overlap_right = brick_right - ball_left
                overlap_top = brick_top - ball_bottom
                overlap_bottom = ball_top - brick_bottom

                min_overlap_x = min(overlap_left, overlap_right)
                min_overlap_y = min(overlap_top, overlap_bottom)

                # Jika benturan dominan horizontal → pantul samping
                if min_overlap_x < min_overlap_y:
                    self.ball.vx *= -1
                    if overlap_left < overlap_right:
                        self.ball.x = brick_left - self.ball.radius - 0.01
                    else:
                        self.ball.x = brick_right + self.ball.radius + 0.01
                else:
                    # Benturan vertikal
                    self.ball.vy *= -1
                    if overlap_bottom < overlap_top:
                        self.ball.y = brick_bottom - self.ball.radius - 0.01
                    else:
                        self.ball.y = brick_top + self.ball.radius + 0.01

                # Hancurkan brick
                self.bricks[i] = None
                break

    def _reset_ball(self):
        """Kembalikan bola ke posisi awal di atas paddle"""
        self.ball.stick_to_paddle = True
        self.ball.vx = 0
        self.ball.vy = 0
        self.ball.x = self.paddle.x
        self.ball.y = self.paddle.y + 2 * self.ball.radius

    def _reset_game(self):
        """Reset game sepenuhnya"""
        self.lives = 3
        self.game_over = False
        self.game_won = False
        self.bricks = self._create_bricks(5, 7)
        self._reset_ball()
        pygame.display.set_caption(f"Arkanoid 3D | Lives: {self.lives}")

    def setup_camera(self):
        """Set konfigurasi perspektif & rotasi kamera OpenGL"""
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
        """Main game loop"""
        clock = pygame.time.Clock()
        running = True

        while running:
            # Event
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                self.handle_mouse(event)

                # Restart jika menang/kalah
                if event.type == KEYDOWN:
                    if (self.game_over or self.game_won) and event.key == K_r:
                        self._reset_game()

            # Update jika game masih berjalan
            if not self.game_over and not self.game_won:
                self.handle_input()
                dt = clock.get_time() / 1000.0

                self.ball.update(dt, self.table.width, self.table.height)
                self._check_paddle_collision()
                self._check_brick_collision()

                # Cek jika bola jatuh keluar area
                bottom_limit = -self.table.height / 2
                if self.ball.y + self.ball.radius < bottom_limit:
                    self.lives -= 1

                    if self.lives > 0:
                        print(f"Bola Jatuh! Sisa nyawa: {self.lives}")
                        self._reset_ball()
                        pygame.display.set_caption(f"Arkanoid 3D | Lives: {self.lives}")
                    else:
                        print("GAME OVER")
                        self.game_over = True
                        pygame.display.set_caption("GAME OVER! Press 'R' to Restart")

                # Cek kondisi menang
                if all(b is None for b in self.bricks):
                    print("YOU WIN!")
                    self.game_won = True
                    pygame.display.set_caption("YOU WIN! Press 'R' to Play Again")

            # Ganti warna background sesuai state
            if self.game_over:
                glClearColor(0.2, 0.0, 0.0, 1.0)
            elif self.game_won:
                glClearColor(0.0, 0.2, 0.0, 1.0)
            else:
                glClearColor(0.0, 0.0, 0.0, 1.0)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.setup_camera()

            # Render objek
            self.table.draw()
            self.paddle.draw()

            if not self.game_over and not self.game_won:
                self.ball.draw()
            elif self.game_won:
                self.ball.draw()  # opsional

            for brick in self.bricks:
                if brick is None:
                    continue
                brick.draw()

            pygame.display.flip()
            clock.tick(self.FRAME_RATE)

        pygame.quit()
