import turtle

# 畫棋盤
def draw_board(n):
    size = 600 / n
    origin = -300

    turtle.setup(700, 700)
    turtle.title(f"{n}x{n} 棋盤")
    turtle.tracer(0)

    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)

    for y in range(n):
        for x in range(n):
            px = origin + x * size
            py = origin + y * size
            pen.penup()
            pen.goto(px, py)
            pen.fillcolor("white" if (x + y) % 2 == 0 else "gray")
            pen.begin_fill()
            pen.pendown()
            for _ in range(4):
                pen.forward(size)
                pen.left(90)
            pen.end_fill()

    turtle.update()

# 放置騎士到 (x, y)
def place_knight(x, y, n):
    size = 600 / n
    origin = -300
    px = origin + x * size + size / 2
    py = origin + y * size + size / 2

    knight = turtle.Turtle()
    knight.shape("turtle")  # 你也可以改成 "circle"
    knight.color("blue")
    knight.penup()
    knight.goto(px, py)

    return knight  # 回傳騎士物件，之後可以移動用

# --- 主程式 ---
def main():
    n = int(input("請輸入想要格數:"))  # 棋盤大小
    draw_board(n)
    knight = place_knight(0, 0, n)  # 騎士預設在左下角 (0, 0)
    
    turtle.mainloop()

main()
