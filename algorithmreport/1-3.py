import turtle
import random

# 騎士可跳的方向
moves = [(-2, -1), (-1, -2), (1, -2), (2, -1),
         (2, 1), (1, 2), (-1, 2), (-2, 1)]

# --- 1. 畫棋盤 ---
def draw_board(n):
    """畫出 n x n 棋盤"""
    size = 600 / n
    origin = -300
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)

    for y in range(n):
        for x in range(n):
            px = origin + x * size
            py = origin + y * size
            pen.penup()
            pen.goto(px, py)
            color = "white" if (x + y) % 2 == 0 else "gray"
            pen.fillcolor(color)
            pen.begin_fill()
            pen.pendown()
            for _ in range(4):
                pen.forward(size)
                pen.left(90)
            pen.end_fill()

# --- 2. 放置騎士 ---
def place_knight(x, y, n):
    """將騎士放在棋盤 (x, y) 格子的中心"""
    size = 600 / n
    origin = -300
    px = origin + x * size + size / 2
    py = origin + y * size + size / 2

    knight = turtle.Turtle()
    knight.shape("circle")
    knight.color("blue")
    knight.penup()
    knight.goto(px, py)
    knight.stamp()
    return knight

# --- 主程式 ---
def main():
    # 1️⃣ 詢問棋盤大小
    while True:
        try:
            n = int(input("1.請輸入棋盤邊長 n（例如 6 表示 6x6 棋盤）："))
            if n >= 1:
                break
            print("請輸入大於等於 1 的整數")
        except ValueError:
            print("請輸入合法整數")

    # 2️⃣ 詢問起點位置
    m = int(input("1.使用 (0, 0) 為起點 2.隨機棋盤上任意位置為起點："))
    if m == 1:
        start_x,start_y = 0,0
    else:
        start_x,start_y = random.randint(0,n-1),random.randint(0,n-1)
    
    print(f"起點位置為：({start_x}, {start_y})")

    # 3️⃣ 初始化畫面與棋盤
    turtle.setup(700, 700)
    turtle.title(f"{n}x{n} 騎士棋盤")
    turtle.tracer(0)
    draw_board(n)
    place_knight(start_x, start_y, n)
    turtle.update()
    turtle.done()

main()
