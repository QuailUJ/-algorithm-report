# 製作棋盤
import turtle

def draw_board(n):
    size = 600 / n  # 自動縮放棋盤大小
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    turtle.tracer(0)

    for y in range(n):
        for x in range(n):
            t.penup()
            t.goto(x * size - 300, y * size - 300)
            t.pendown()
            t.fillcolor('white' if (x + y) % 2 == 0 else 'gray')
            t.begin_fill()
            for _ in range(4):
                t.forward(size)
                t.left(90)
            t.end_fill()

    turtle.update()
    turtle.done()



draw_board(8)  
