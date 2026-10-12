import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


cube_vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

cube_faces = (
    (0, 1, 2, 3),
    (4, 5, 7, 6),
    (0, 4, 5, 1),
    (2, 7, 6, 3),
    (1, 5, 7, 2),
    (0, 4, 6, 3)
)

cube_normals = (
    (0, 0, -1),
    (0, 0, 1),
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0)
)

texture_coords = (
    (0, 0),
    (1, 0),
    (1, 1),
    (0, 1)
)

roof_vertices = (
    (-1.2, 1, -1.2),
    (1.2, 1, -1.2),
    (1.2, 1, 1.2),
    (-1.2, 1, 1.2),
    (0, 2.2, 0)
)

roof_faces = (
    (0, 1, 4),
    (1, 2, 4),
    (2, 3, 4),
    (3, 0, 4),
    (0, 1, 2, 3)
)

roof_normals = (
    (0, 0.7, -0.7),
    (0.7, 0.7, 0),
    (0, 0.7, 0.7),
    (-0.7, 0.7, 0),
    (0, -1, 0)
)

roof_colors = (
    (0.8, 0.2, 0.2, 1),
    (0.9, 0.3, 0.2, 1),
    (0.7, 0.1, 0.1, 1),
    (0.9, 0.4, 0.2, 1),
    (0.5, 0.2, 0.1, 1)
)


def load_texture(filename):
    texture_surface = pygame.image.load(filename)
    texture_data = pygame.image.tostring(
        texture_surface,
        "RGBA",
        True
    )

    width = texture_surface.get_width()
    height = texture_surface.get_height()

    texture_id = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameteri(
        GL_TEXTURE_2D,
        GL_TEXTURE_MIN_FILTER,
        GL_LINEAR
    )

    glTexParameteri(
        GL_TEXTURE_2D,
        GL_TEXTURE_MAG_FILTER,
        GL_LINEAR
    )

    glTexParameteri(
        GL_TEXTURE_2D,
        GL_TEXTURE_WRAP_S,
        GL_REPEAT
    )

    glTexParameteri(
        GL_TEXTURE_2D,
        GL_TEXTURE_WRAP_T,
        GL_REPEAT
    )

    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        width,
        height,
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        texture_data
    )

    return texture_id


def set_material(color):
    glMaterialfv(
        GL_FRONT_AND_BACK,
        GL_AMBIENT_AND_DIFFUSE,
        color
    )

    glMaterialfv(
        GL_FRONT_AND_BACK,
        GL_SPECULAR,
        (0.3, 0.3, 0.3, 1)
    )

    glMaterialf(
        GL_FRONT_AND_BACK,
        GL_SHININESS,
        32
    )


def draw_cube(texture_id):
    glEnable(GL_TEXTURE_2D)

    glBindTexture(GL_TEXTURE_2D, texture_id)

    glColor4f(1, 1, 1, 1)

    glMaterialfv(
        GL_FRONT_AND_BACK,
        GL_AMBIENT_AND_DIFFUSE,
        (1, 1, 1, 1)
    )

    glBegin(GL_QUADS)

    for i, face in enumerate(cube_faces):
        glNormal3fv(cube_normals[i])

        for j, vertex in enumerate(face):
            glTexCoord2fv(texture_coords[j])
            glVertex3fv(cube_vertices[vertex])

    glEnd()

    glDisable(GL_TEXTURE_2D)


def draw_roof():
    glBegin(GL_TRIANGLES)

    for i in range(4):
        set_material(roof_colors[i])
        glNormal3fv(roof_normals[i])

        for vertex in roof_faces[i]:
            glVertex3fv(roof_vertices[vertex])

    glEnd()

    glBegin(GL_QUADS)

    set_material(roof_colors[4])
    glNormal3fv(roof_normals[4])

    for vertex in roof_faces[4]:
        glVertex3fv(roof_vertices[vertex])

    glEnd()


def draw_house(texture_id):
    draw_cube(texture_id)
    draw_roof()


pygame.init()

display = (900, 700)

pygame.display.set_mode(
    display,
    DOUBLEBUF | OPENGL
)

pygame.display.set_caption(
    "Лабораторная работа 4 - OpenGL"
)

glEnable(GL_DEPTH_TEST)

glClearColor(0.75, 0.9, 1.0, 1.0)

glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glEnable(GL_NORMALIZE)

glLightfv(
    GL_LIGHT0,
    GL_AMBIENT,
    (0.25, 0.25, 0.25, 1)
)

glLightfv(
    GL_LIGHT0,
    GL_DIFFUSE,
    (0.9, 0.9, 0.9, 1)
)

glLightfv(
    GL_LIGHT0,
    GL_SPECULAR,
    (1, 1, 1, 1)
)

glMatrixMode(GL_PROJECTION)

glLoadIdentity()

gluPerspective(
    45,
    display[0] / display[1],
    0.1,
    50.0
)

glMatrixMode(GL_MODELVIEW)

texture_id = load_texture("meme.png")

distance = -8

rotation_x = 20
rotation_y = 30
rotation_z = 0

auto_rotate = True

mouse_dragging = False

last_mouse_x = 0
last_mouse_y = 0

clock = pygame.time.Clock()

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                running = False

            if event.key == K_SPACE:
                auto_rotate = not auto_rotate

        if event.type == MOUSEBUTTONDOWN:

            if event.button == 1:
                mouse_dragging = True
                last_mouse_x, last_mouse_y = event.pos

        if event.type == MOUSEBUTTONUP:

            if event.button == 1:
                mouse_dragging = False

        if event.type == MOUSEMOTION and mouse_dragging:

            mouse_x, mouse_y = event.pos

            dx = mouse_x - last_mouse_x
            dy = mouse_y - last_mouse_y

            rotation_y += dx * 0.5
            rotation_x += dy * 0.5

            last_mouse_x = mouse_x
            last_mouse_y = mouse_y

    keys = pygame.key.get_pressed()

    if keys[K_LEFT]:
        rotation_y -= 2

    if keys[K_RIGHT]:
        rotation_y += 2

    if keys[K_UP]:
        rotation_x -= 2

    if keys[K_DOWN]:
        rotation_x += 2

    if keys[K_q]:
        rotation_z -= 2

    if keys[K_e]:
        rotation_z += 2

    if keys[K_w]:
        distance += 0.08

    if keys[K_s]:
        distance -= 0.08

    if auto_rotate and not mouse_dragging:
        rotation_y += 0.4

    glClear(
        GL_COLOR_BUFFER_BIT |
        GL_DEPTH_BUFFER_BIT
    )

    glLoadIdentity()

    glLightfv(
        GL_LIGHT0,
        GL_POSITION,
        (4, 5, 6, 1)
    )

    glTranslatef(
        0,
        -0.3,
        distance
    )

    glRotatef(
        rotation_x,
        1,
        0,
        0
    )

    glRotatef(
        rotation_y,
        0,
        1,
        0
    )

    glRotatef(
        rotation_z,
        0,
        0,
        1
    )

    draw_house(texture_id)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()