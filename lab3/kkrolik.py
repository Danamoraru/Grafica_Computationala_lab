import pygame
import numpy as np
import sys

pygame.init()

WIDTH = 700
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Julia Set - Douady Rabbit")

font = pygame.font.SysFont("Arial", 18)

C_REAL = -0.123
C_IMAG = 0.745

center_x = 0.0
center_y = 0.0
view_size = 3.2
zoom_level = 1.0

try:
    max_iterations = int(input("Введите количество итераций: "))
except:
    max_iterations = 100

max_iterations = max(10, max_iterations)


def draw_fractal():
    x = np.linspace(
        center_x - view_size / 2,
        center_x + view_size / 2,
        WIDTH
    )

    y = np.linspace(
        center_y - view_size / 2,
        center_y + view_size / 2,
        HEIGHT
    )

    X, Y = np.meshgrid(x, y)

    Z = X + 1j * Y
    C = C_REAL + 1j * C_IMAG

    iterations = np.zeros(Z.shape, dtype=np.int32)
    active = np.ones(Z.shape, dtype=bool)

    for i in range(max_iterations):
        Z[active] = Z[active] * Z[active] + C

        escaped = (
            Z.real * Z.real +
            Z.imag * Z.imag
        ) > 4

        new_escaped = escaped & active

        iterations[new_escaped] = i

        active &= ~escaped

        if not active.any():
            break

    iterations[active] = max_iterations

    t = iterations / max_iterations

    image = np.zeros(
        (HEIGHT, WIDTH, 3),
        dtype=np.uint8
    )

    mask1 = (t < 0.33) & (~active)
    mask2 = (t >= 0.33) & (t < 0.66) & (~active)
    mask3 = (t >= 0.66) & (~active)

    k1 = t[mask1] / 0.33

    image[mask1, 0] = 35 + 90 * k1
    image[mask1, 1] = 20 + 20 * k1
    image[mask1, 2] = 80 + 100 * k1

    k2 = (t[mask2] - 0.33) / 0.33

    image[mask2, 0] = 125 + 100 * k2
    image[mask2, 1] = 40 + 70 * k2
    image[mask2, 2] = 180 - 40 * k2

    k3 = (t[mask3] - 0.66) / 0.34

    image[mask3, 0] = 225
    image[mask3, 1] = 110 + 110 * k3
    image[mask3, 2] = 140 - 70 * k3

    image[active] = (8, 8, 18)

    surface = pygame.surfarray.make_surface(
        np.transpose(image, (1, 0, 2))
    )

    screen.blit(surface, (0, 0))

    panel = pygame.Surface(
        (WIDTH, 75),
        pygame.SRCALPHA
    )

    panel.fill((0, 0, 0, 180))

    screen.blit(panel, (0, 0))

    text1 = font.render(
        f"Zoom: {zoom_level:.2f}x",
        True,
        (255, 255, 255)
    )

    text2 = font.render(
        f"Center: ({center_x:.6f}, {center_y:.6f})",
        True,
        (255, 255, 255)
    )

    text3 = font.render(
        f"Iterations: {max_iterations}   +/- change   R reset",
        True,
        (255, 255, 255)
    )

    screen.blit(text1, (10, 5))
    screen.blit(text2, (10, 28))
    screen.blit(text3, (10, 51))

    pygame.display.flip()


def reset():
    global center_x
    global center_y
    global view_size
    global zoom_level

    center_x = 0.0
    center_y = 0.0
    view_size = 3.2
    zoom_level = 1.0


draw_fractal()

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                mouse_x, mouse_y = event.pos

                center_x += (
                    mouse_x - WIDTH / 2
                ) * view_size / WIDTH

                center_y += (
                    mouse_y - HEIGHT / 2
                ) * view_size / HEIGHT

                view_size /= 2
                zoom_level *= 2

                draw_fractal()

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:

                reset()

                draw_fractal()

            elif event.key in (
                pygame.K_EQUALS,
                pygame.K_KP_PLUS
            ):

                max_iterations += 20

                draw_fractal()

            elif event.key in (
                pygame.K_MINUS,
                pygame.K_KP_MINUS
            ):

                max_iterations = max(
                    20,
                    max_iterations - 20
                )

                draw_fractal()

pygame.quit()
sys.exit()