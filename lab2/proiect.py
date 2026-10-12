import turtle
import math

MAX_ORDER = 10
DEFAULT_ORDER = 4

LEVEL_COLORS = (
    "#2d6a4f",
    "#40916c",
    "#52b788",
    "#74c69d",
    "#95d5b2",
    "#b7e4c7",
    "#d8f3dc",
    "#f4a261",
    "#e9c46a",
    "#e76f51",
    "#9b5de5",
)


def draw_square(pen, x, y, size, angle, color):
    pen.penup()
    pen.goto(x, y)
    pen.setheading(angle)

    pen.pendown()
    pen.pencolor(color)
    pen.fillcolor(color)

    pen.begin_fill()

    for _ in range(4):
        pen.forward(size)
        pen.left(90)

    pen.end_fill()




def pythagoras_tree(pen, x, y, size, angle, level, max_level, counter):


    color = LEVEL_COLORS[level % len(LEVEL_COLORS)]

    draw_square(
        pen,
        x,
        y,
        size,
        angle,
        color
    )

    counter[0] += 1

   
    if level >= max_level:
        return


    rad = math.radians(angle)

    left_x = x - size * math.sin(rad)
    left_y = y + size * math.cos(rad)

    
    new_size = size / math.sqrt(2)

   
    angle_left = angle + 45

    pythagoras_tree(
        pen,
        left_x,
        left_y,
        new_size,
        angle_left,
        level + 1,
        max_level,
        counter
    )


    rad_left = math.radians(angle_left)

    right_x = left_x + new_size * math.cos(rad_left)
    right_y = left_y + new_size * math.sin(rad_left)

  
    angle_right = angle - 45

    pythagoras_tree(
        pen,
        right_x,
        right_y,
        new_size,
        angle_right,
        level + 1,
        max_level,
        counter
    )




def draw_tree(screen, pen, info, order):

    pen.clear()
    info.clear()

    counter = [0]


    start_size = 120


    start_x = -start_size / 2
    start_y = -300

    pythagoras_tree(
        pen,
        start_x,
        start_y,
        start_size,
        0,
        0,
        order,
        counter
    )

  
    info.write(
        f"Adancimea N: {order}    Numar de patrate: {counter[0]}",
        align="left",
        font=("Arial", 14, "bold")
    )

    screen.update()



def main():

    screen = turtle.Screen()

    screen.title(
        "Arborele lui Pitagora | + / - sau sagetile Sus / Jos"
    )

    screen.setup(
        width=1000,
        height=750
    )

    screen.bgcolor("#101820")


    screen.tracer(0, 0)

    # crearea cursorului care deseneaza
    pen = turtle.Turtle()

    pen.hideturtle()
    pen.speed(0)

    # cursor pentru informatii
    info = turtle.Turtle(visible=False)

    info.penup()
    info.color("white")

    info.goto(
        -screen.window_width() // 2 + 20,
        screen.window_height() // 2 - 45
    )

    # utilizatorul introduce adancimea
    answer = screen.textinput(
        "Arborele lui Pitagora",
        f"Introdu adancimea N de la 0 la {MAX_ORDER}:"
    )

    try:

        if answer is not None:

            order = int(answer)

            order = max(
                0,
                min(MAX_ORDER, order)
            )

        else:

            order = DEFAULT_ORDER

    except ValueError:

        order = DEFAULT_ORDER



    def change_order(amount):

        nonlocal order

        order = max(
            0,
            min(MAX_ORDER, order + amount)
        )

        draw_tree(
            screen,
            pen,
            info,
            order
        )


    # prima desenare
    draw_tree(
        screen,
        pen,
        info,
        order
    )
   

    screen.listen()

    # cresterea adancimii
    for key in ("plus", "equal", "Up", "KP_Add"):

        screen.onkeypress(
            lambda: change_order(1),
            key
        )

    # scaderea adancimii
    for key in ("minus", "underscore", "Down", "KP_Subtract"):

        screen.onkeypress(
            lambda: change_order(-1),
            key
        )


    screen.mainloop()


if __name__ == "__main__":
    main()