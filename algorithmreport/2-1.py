import turtle
import random
import time

# 騎士可跳的方向
moves = [(-2, -1), (-1, -2), (1, -2), (2, -1),
         (2, 1), (1, 2), (-1, 2), (-2, 1)]

# --- 1. 畫棋盤 ---
BOARD_PIXEL_WIDTH = 600

def draw_board(n):
    """畫出 n x n 的棋盤"""
    size = BOARD_PIXEL_WIDTH / n
    origin = -BOARD_PIXEL_WIDTH / 2
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
    """將騎士放在棋盤 (x, y) 格子的中心位置"""
    size = BOARD_PIXEL_WIDTH / n
    origin = -BOARD_PIXEL_WIDTH / 2
    px = origin + x * size + size / 2
    py = origin + y * size + size / 2

    knight = turtle.Turtle()
    knight.shape("circle")
    knight.shapesize(2.5, 2.5, 2.5)
    knight.color("blue")
    knight.penup()
    knight.goto(px, py)
    knight.stamp()
    return knight

# --- 3. Warnsdorff 規則動畫 + 畫路徑 ---
def run_warnsdorff_animation(n, start_x, start_y):
    """騎士巡遊動畫 + 逐步連線顯示路徑"""
    board = [[0] * n for _ in range(n)]
    x, y = start_x, start_y
    size = BOARD_PIXEL_WIDTH / n
    origin = -BOARD_PIXEL_WIDTH / 2

    # 騎士物件
    knight = turtle.Turtle()
    knight.shape("circle")
    knight.color("pink")
    knight.penup()
    knight.speed(1)

    # 寫步數用筆
    writer = turtle.Turtle()
    writer.hideturtle()
    writer.penup()
    writer.color("blue")

    # 畫線筆
    path_pen = turtle.Turtle()
    path_pen.hideturtle()
    path_pen.color("black")
    path_pen.width(2)
    path_pen.speed(0)
    path_pen.penup()

    # 殘影
    trail = turtle.Turtle()
    trail.hideturtle()
    trail.penup()
    trail.color("cyan")     # 殘影顏色，可用 lightblue, cyan, etc.
    trail.speed(0)
    # 在每一步中加入：
    




    prev_px = prev_py = None  # 前一格中心座標

    for step in range(1, n * n + 1):
        board[y][x] = step
        # 計算這格中心座標
        px = origin + x * size + size / 2
        py = origin + y * size + size / 2

        # 畫線：從前一步連到這一步
        if prev_px is not None:
            path_pen.goto(prev_px, prev_py)
            path_pen.pendown()
            path_pen.goto(px, py)
            path_pen.penup()
        prev_px, prev_py = px, py  # 更新前一步座標

        # 騎士移動 + 步數顯示
        knight.goto(px, py)
        knight.stamp()

        trail.goto(px, py)
        trail.dot(size * 0.6)   # 畫一個淡淡圓形殘影，大小根據格子比例

        writer.goto(px, py - size / 4)
        writer.write(str(step), align="center", font=("Arial", int(size / 5), "normal"))
        time.sleep(0.1)

        # 計算下一步
        candidates = []
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and board[ny][nx] == 0:
                count = sum(
                    1 for ddx, ddy in moves
                    if 0 <= nx + ddx < n and 0 <= ny + ddy < n and board[ny + ddy][nx + ddx] == 0
                )
                candidates.append((count, nx, ny))

        if not candidates:
            break
        candidates.sort()
        _, x, y = candidates[0]

# --- 主程式 ---
def main():
    while True:
        try:
            n = int(input("1.請輸入棋盤邊長 n（例如 6 表示 6x6 棋盤）："))
            if n >= 1:
                break
            print("請輸入大於等於 1 的整數")
        except ValueError:
            print("請輸入合法整數")

    m = int(input("2.選擇起點：1 表示 (0,0)；2 表示隨機位置："))
    if m == 1:
        start_x, start_y = 0, 0
    else:
        start_x = random.randint(0, n - 1)
        start_y = random.randint(0, n - 1)

    print(f"✅ 起點位置為：({start_x}, {start_y})")

    turtle.setup(BOARD_PIXEL_WIDTH+200,BOARD_PIXEL_WIDTH+200)
    turtle.title(f"{n}x{n} 騎士巡遊動畫 - Warnsdorff")
    turtle.tracer(0)
    draw_board(n)
    turtle.update()
    run_warnsdorff_animation(n, start_x, start_y)
    turtle.done()

main()
