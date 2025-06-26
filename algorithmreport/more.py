import turtle
import random
import time
import multiprocessing
import tkinter as TK

# 騎士可跳的方向
moves = [(-2, -1), (-1, -2), (1, -2), (2, -1),
         (2, 1), (1, 2), (-1, 2), (-2, 1)]

# Warnsdorff 演算法
def warnsdorff_path(n, start_x, start_y):
    board = [[0] * n for _ in range(n)]
    x, y = start_x, start_y
    path = []
    for step in range(1, n * n + 1):
        board[y][x] = step
        path.append((x, y, step))
        candidates = []
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and board[ny][nx] == 0:
                onward = sum(1 for ddx, ddy in moves
                             if 0 <= nx + ddx < n and 0 <= ny + ddy < n and board[ny + ddy][nx + ddx] == 0)
                candidates.append((onward, nx, ny))
        if not candidates:
            break
        candidates.sort()
        _, x, y = candidates[0]
    return path

# 每個棋盤的動畫函式
def run_one_board(x_offset, y_offset):
    n = 8
    size = 40
    turtle.setup(40, 40)
    turtle.title("騎士巡遊視窗")
    turtle.bgcolor("black")
    turtle.speed(0)
    turtle.tracer(0)

    # 設定視窗位置
    root = turtle.Screen()._root
    root.geometry(f"400x400+{x_offset}+{y_offset}")

    pen = turtle.Turtle()
    pen.hideturtle()
    for y in range(n):
        for x in range(n):
            pen.penup()
            pen.goto(x * size - 160, y * size - 160)
            pen.fillcolor("white" if (x + y) % 2 == 0 else "gray")
            pen.begin_fill()
            pen.pendown()
            for _ in range(4):
                pen.forward(size)
                pen.left(90)
            pen.end_fill()
    turtle.update()

    # 隨機起點
    sx, sy = random.randint(0, n - 1), random.randint(0, n - 1)
    path = warnsdorff_path(n, sx, sy)

    knight = turtle.Turtle()
    knight.shape("circle")
    knight.color("purple")
    knight.penup()
    knight.turtlesize(1.5)
    knight.speed(0)

    trail = turtle.Turtle()
    trail.hideturtle()
    trail.penup()
    trail.color("cyan")
    trail.speed(0)

    connector = turtle.Turtle()
    connector.hideturtle()
    connector.penup()
    connector.color("red")
    connector.pensize(2)

    writer = turtle.Turtle()
    writer.hideturtle()
    writer.penup()
    writer.color("black")

    prev = None
    for x, y, step in path:
        px = x * size - 160 + size / 2
        py = y * size - 160 + size / 2
        knight.goto(px, py)
        knight.stamp()
        writer.goto(px, py - size / 4)
        writer.write(str(step), align="center", font=("Arial", 8, "normal"))
        if prev:
            connector.goto(*prev)
            connector.pendown()
            connector.goto(px, py)
            connector.penup()
        trail.goto(px, py)
        trail.dot(size * 0.6)
        prev = (px, py)
        time.sleep(0.05)

    turtle.done()

# 主程式：開 16 個隨機位置棋盤
if __name__ == "__main__":
    processes = []
    screen_width = 2560   # 螢幕總寬度 (你可以依自己螢幕大小調整)
    screen_height = 1920   # 螢幕總高度

    cols = 4
    rows = 4
    win_w = 400
    win_h = 400

    for i in range(16):
        col = i % cols
        row = i // cols
        x_offset = col * win_w
        y_offset = row * win_h
        p = multiprocessing.Process(target=run_one_board, args=(x_offset, y_offset))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()