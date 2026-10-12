
import pygame
import math

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Walking Girl")
clock = pygame.time.Clock()

BG = (236, 244, 255)
GRASS = (120, 195, 120)
BLACK = (45, 45, 60)
WHITE = (255, 255, 255)
SKIN = (255, 222, 190)
HAIR = (105, 68, 46)
PINK = (235, 110, 170)
DARK_PINK = (190, 65, 125)
SHOES = (80, 65, 90)
CHEEKS = (255, 175, 190)

GROUND = 510

x = WIDTH / 2
speed = 0.0
walk_speed = 5.0
run_speed = 9.0
acceleration = 0.30
friction = 0.20
direction = 1

phase = 0.0
swing = 0.0

jump_height = 0.0
jump_velocity = 0.0
gravity = 0.55
jump_power = -12

font = pygame.font.SysFont("Arial", 23)
title_font = pygame.font.SysFont("Arial", 28, bold=True)


def point(cx, cy, dx, dy, direction=1):
    return (
        round(cx + dx * direction),
        round(cy + dy)
    )


def draw_background():
    screen.fill(BG)

    pygame.draw.circle(
        screen, (255, 225, 120), (790, 90), 40
    )

    for cx, cy in [(180, 100), (540, 115)]:
        pygame.draw.circle(screen, WHITE, (cx - 25, cy), 25)
        pygame.draw.circle(screen, WHITE, (cx, cy - 12), 33)
        pygame.draw.circle(screen, WHITE, (cx + 30, cy), 24)

    pygame.draw.rect(
        screen, GRASS,
        (0, GROUND + 2, WIDTH, HEIGHT - GROUND)
    )

    pygame.draw.line(
        screen, (80, 145, 85),
        (0, GROUND + 2),
        (WIDTH, GROUND + 2), 2
    )


def draw_character(cx, ground_y, swing, direction):

    def p(dx, dy):
        return point(cx, ground_y, dx, dy, direction)

    leg_shift = swing * 17

    left_knee = p(-10 + leg_shift * 0.4, -28)
    right_knee = p(10 - leg_shift * 0.4, -28)

    left_foot = p(-12 + leg_shift, -4)
    right_foot = p(12 - leg_shift, -4)

    pygame.draw.line(screen, SKIN, p(-9, -64), left_knee, 7)
    pygame.draw.line(screen, SKIN, left_knee, left_foot, 7)

    pygame.draw.line(screen, SKIN, p(9, -64), right_knee, 7)
    pygame.draw.line(screen, SKIN, right_knee, right_foot, 7)

    pygame.draw.ellipse(
        screen, SHOES,
        (left_foot[0] - 9, left_foot[1] - 3, 19, 9)
    )
    pygame.draw.ellipse(
        screen, SHOES,
        (right_foot[0] - 9, right_foot[1] - 3, 19, 9)
    )

    arm_shift = swing * 12

    left_shoulder = p(-15, -103)
    right_shoulder = p(15, -103)

    left_hand = p(-28 + arm_shift, -72)
    right_hand = p(28 - arm_shift, -72)

    pygame.draw.line(
        screen, SKIN, left_shoulder, left_hand, 7
    )
    pygame.draw.line(
        screen, SKIN, right_shoulder, right_hand, 7
    )

    pygame.draw.circle(screen, SKIN, left_hand, 5)
    pygame.draw.circle(screen, SKIN, right_hand, 5)

    pygame.draw.rect(
        screen, SKIN,
        (round(cx - 6), round(ground_y - 123), 12, 19),
        border_radius=4
    )

    dress = [
        p(-13, -109),
        p(13, -109),
        p(16, -91),
        p(24, -76),
        p(33, -57),
        p(-33, -57),
        p(-24, -76),
        p(-16, -91)
    ]

    pygame.draw.polygon(screen, PINK, dress)
    pygame.draw.polygon(screen, DARK_PINK, dress, 2)

    pygame.draw.line(
        screen, DARK_PINK,
        p(-17, -88), p(17, -88), 4
    )

    for side in (-1, 1):
        sleeve = [
            p(side * 13, -108),
            p(side * 22, -103),
            p(side * 24, -91),
            p(side * 15, -94)
        ]
        pygame.draw.polygon(screen, PINK, sleeve)
        pygame.draw.polygon(screen, DARK_PINK, sleeve, 2)

    pygame.draw.polygon(
        screen, WHITE,
        [p(-7, -109), p(0, -100), p(7, -109)]
    )

    pygame.draw.ellipse(
        screen, HAIR,
        (round(cx - 23), round(ground_y - 165), 46, 41)
    )

    pygame.draw.line(
        screen, HAIR,
        p(-19, -142), p(-21, -114), 9
    )
    pygame.draw.line(
        screen, HAIR,
        p(19, -142), p(21, -114), 9
    )

    head = p(0, -146)
    pygame.draw.circle(screen, SKIN, head, 20)

    pygame.draw.ellipse(
        screen, HAIR,
        (round(cx - 19), round(ground_y - 167), 38, 12)
    )

    left_eye = p(-8, -148)
    right_eye = p(8, -148)

    pygame.draw.circle(screen, WHITE, left_eye, 5)
    pygame.draw.circle(screen, WHITE, right_eye, 5)

    pupil = 2 if direction == 1 else -2

    pygame.draw.circle(
        screen, BLACK,
        (left_eye[0] + pupil, left_eye[1]), 3
    )
    pygame.draw.circle(
        screen, BLACK,
        (right_eye[0] + pupil, right_eye[1]), 3
    )

    pygame.draw.circle(screen, CHEEKS, p(-13, -138), 4)
    pygame.draw.circle(screen, CHEEKS, p(13, -138), 4)

    pygame.draw.arc(
        screen, DARK_PINK,
        (round(cx - 7), round(ground_y - 139), 14, 9),
        math.pi, 2 * math.pi, 2
    )


def draw_hud(speed, direction, jumping, running):

    pygame.draw.rect(
        screen, WHITE,
        (12, 12, 350, 175),
        border_radius=14
    )

    pygame.draw.rect(
        screen, PINK,
        (12, 12, 350, 175),
        2,
        border_radius=14
    )

    state = "Jumping" if jumping else "On ground"
    movement = "Running" if running else "Walking"

    texts = [
        ("Walking Girl", DARK_PINK, 20, title_font),
        (f"Speed: {abs(speed):.2f} px/frame", BLACK, 58, font),
        (f"Direction: {'Right' if direction == 1 else 'Left'}", BLACK, 90, font),
        (f"State: {state}", BLACK, 120, font),
        (f"Mode: {movement}", BLACK, 150, font)
    ]

    for message, color, ypos, used_font in texts:
        surface = used_font.render(message, True, color)
        screen.blit(surface, (27, ypos))

   

running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if jump_height == 0 and jump_velocity == 0:
                    jump_velocity = jump_power

    keys = pygame.key.get_pressed()

    left = keys[pygame.K_a] or keys[pygame.K_LEFT]
    right = keys[pygame.K_d] or keys[pygame.K_RIGHT]

    shift_pressed = (
        keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
    )

    max_speed = run_speed if shift_pressed else walk_speed

    moving = left != right

    if left and not right:
        speed -= acceleration
        direction = -1

    elif right and not left:
        speed += acceleration
        direction = 1

    else:
        if speed > 0:
            speed = max(0, speed - friction)
        elif speed < 0:
            speed = min(0, speed + friction)

    speed = max(-max_speed, min(max_speed, speed))

    x += speed

    if x < 45:
        x = 45
        speed = 0
    elif x > WIDTH - 45:
        x = WIDTH - 45
        speed = 0

    if jump_height < 0 or jump_velocity != 0:
        jump_height += jump_velocity
        jump_velocity += gravity

        if jump_height >= 0:
            jump_height = 0
            jump_velocity = 0

    if moving and abs(speed) > 0:
        phase += abs(speed) * 0.12
        swing = math.sin(phase)
    else:
        phase = 0.0
        swing = 0.0

    draw_background()

    draw_character(
        x,
        GROUND + jump_height,
        swing,
        direction
    )

    draw_hud(
        speed,
        direction,
        jump_height < 0,
        shift_pressed
    )

    pygame.display.flip()

pygame.quit()
