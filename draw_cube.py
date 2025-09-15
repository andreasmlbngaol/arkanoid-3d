from OpenGL.GL import *


# ========================
# Helper untuk balok (cube)
# ========================
def draw_cube(w, h, d, color=(1, 1, 1)):
    glColor3f(*color)
    vertices = [
        [-w/2, -h/2, -d/2],
        [ w/2, -h/2, -d/2],
        [ w/2,  h/2, -d/2],
        [-w/2,  h/2, -d/2],
        [-w/2, -h/2,  d/2],
        [ w/2, -h/2,  d/2],
        [ w/2,  h/2,  d/2],
        [-w/2,  h/2,  d/2],
    ]
    faces = [
        (0,1,2,3),
        (4,5,6,7),
        (0,1,5,4),
        (2,3,7,6),
        (1,2,6,5),
        (0,3,7,4),
    ]
    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()
