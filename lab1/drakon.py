import turtle


MAX_ORDER = 12
DEFAULT_ORDER = 4
LEVEL_COLORS = (
    "#e76f51",
    "#f4a261",
    "#e9c46a",
    "#a8dadc",
    "#457b9d",
    "#9b5de5",
    "#00bbf9",
    "#00f5d4",
    "#80ed99",
    "#f15bb5",
    "#fee440",
    "#b8f2e6",
    "#f7aef8",
)

#штука для поврота на 90
def dragon_turns(order):
    if order == 0:
        return []

    turns = dragon_turns(order - 1)
    return turns + [1] + [-turn for turn in reversed(turns)]

#кароче перевод в x,y кординаты
def curve_points(order):
    points = [(0, 0)]
    x, y = 0, 0
    heading = 0

    for turn in dragon_turns(order):
        if heading == 0:
            x += 1
        elif heading == 90:
            y += 1
        elif heading == 180:
            x -= 1
        else:
            y -= 1
        points.append((x, y))
        heading = (heading + turn * 90) % 360

    if not dragon_turns(order):
        points.append((1, 0))
    else:
        if heading == 0:
            x += 1
        elif heading == 90:
            y += 1
        elif heading == 180:
            x -= 1
        else:
            y -= 1
        points.append((x, y))

    return points

#типо чтобы было по центру
def draw_curve(screen, pen, info, order):
    points = curve_points(order)
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    width = max(1, screen.window_width() - 80)
    height = max(1, screen.window_height() - 130)
    scale = min(
        width / max(1, max_x - min_x),
        height / max(1, max_y - min_y),
    )
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
#рисовалка
    pen.clear()
    pen.penup()
    pen.goto((points[0][0] - center_x) * scale, (points[0][1] - center_y) * scale - 30)
    pen.pendown()
    screen.update()

    update_interval = max(1, len(points) // 150)
    previous_point = points[0]
    for segment_index, point in enumerate(points[1:]):
        level = max(0, order - segment_index.bit_length())
        pen.pencolor(LEVEL_COLORS[level])
        dx = point[0] - previous_point[0]
        dy = point[1] - previous_point[1]
        pen.setheading(0 if dx > 0 else 180 if dx < 0 else 90 if dy > 0 else 270)
        pen.goto((point[0] - center_x) * scale, (point[1] - center_y) * scale - 30)
        previous_point = point
        if (segment_index + 1) % update_interval == 0:
            screen.update()
#вывод инфы
    info.clear()
    info.write(
        f"Глубина N: {order}    Элементов: {len(points) - 1}",
        align="left",
        font=("Arial", 14, "bold"),
    )
    screen.update()

#штука как пользоватся
def main():
    screen = turtle.Screen()
    screen.title("Кривая дракона | + / - или стрелки вверх / вниз")
    screen.setup(width=1000, height=700)
    screen.bgcolor("#101820")
    screen.tracer(0, 0)

    pen = turtle.Turtle(shape="turtle")
    pen.speed(0)
    pen.pensize(2)
    pen.fillcolor("white")

    info = turtle.Turtle(visible=False)
    info.penup()
    info.color("white")
    info.goto(-screen.window_width() // 2 + 20, screen.window_height() // 2 - 45)

    answer = screen.textinput("Кривая дракона", f"Глубина N от 0 до {MAX_ORDER}:")
    try:
        order = max(0, min(MAX_ORDER, int(answer))) if answer is not None else DEFAULT_ORDER
    except ValueError:
        order = DEFAULT_ORDER

    def change_order(amount):
        nonlocal order
        order = max(0, min(MAX_ORDER, order + amount))
        draw_curve(screen, pen, info, order)

    draw_curve(screen, pen, info, order)
    screen.listen()
    for key in ("plus", "equal", "Up", "KP_Add"):
        screen.onkeypress(lambda: change_order(1), key)
    for key in ("minus", "underscore", "Down", "KP_Subtract"):
        screen.onkeypress(lambda: change_order(-1), key)
    screen.mainloop()


if __name__ == "__main__":
    main()