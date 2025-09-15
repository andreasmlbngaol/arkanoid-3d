import pygame
from OpenGL.GL import *

class Table:
    def __init__(self, width=8, height=10, depth=0.5, texture_file="background.jpg"):
        self.width = width
        self.height = height
        self.depth = depth
        self.texture_id = self._load_texture(texture_file)

    def _load_texture(self, file):
        texture_surface = pygame.image.load(file)
        texture_data = pygame.image.tostring(texture_surface, "RGB", True)
        width = texture_surface.get_width()
        height = texture_surface.get_height()

        texid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texid)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                     0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        return texid

    def draw(self):
        width = self.width / 2
        height = self.height / 2
        depth = self.depth

        # --- DEPAN (pakai tekstur) ---
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glColor3f(1, 1, 1) # putih (biar warna asli tekstur nggak ketimpa)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(-width, -height, 0)
        glTexCoord2f(1, 0); glVertex3f( width, -height, 0)
        glTexCoord2f(1, 1); glVertex3f( width,  height, 0)
        glTexCoord2f(0, 1); glVertex3f(-width,  height, 0)
        glEnd()

        glDisable(GL_TEXTURE_2D)

        # --- BELAKANG ---
        glColor3f(0.2,  0.2, 0.2)  # abu-abu
        glBegin(GL_QUADS)
        glVertex3f(-width, -height, -depth)
        glVertex3f( width, -height, -depth)
        glVertex3f( width,  height, -depth)
        glVertex3f(-width,  height, -depth)
        glEnd()

        # --- KIRI ---
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_QUADS)
        glVertex3f(-width, -height, -depth)
        glVertex3f(-width, -height,  depth)
        glVertex3f(-width,  height,  depth)
        glVertex3f(-width,  height, -depth)
        glEnd()

        # --- KANAN ---
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_QUADS)
        glVertex3f(width, -height, -depth)
        glVertex3f(width, -height,  depth)
        glVertex3f(width,  height,  depth)
        glVertex3f(width,  height, -depth)
        glEnd()

        # --- ATAS ---
        glColor3f(0.4, 0.4, 0.4)
        glBegin(GL_QUADS)
        glVertex3f(-width, height, -depth)
        glVertex3f( width, height, -depth)
        glVertex3f( width, height,  depth)
        glVertex3f(-width, height,  depth)
        glEnd()

        # --- BAWAH ---
        glColor3f(0.4, 0.4, 0.4)
        glBegin(GL_QUADS)
        glVertex3f(-width, -height, -depth)
        glVertex3f( width, -height, -depth)
        glVertex3f( width, -height,  depth)
        glVertex3f(-width, -height,  depth)
        glEnd()
