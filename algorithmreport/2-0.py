import turtle
import random
import time

# 騎士可跳的方向，共 8 種「ㄇ」字型走法
moves = [(-2, -1), (-1, -2), (1, -2), (2, -1),
         (2, 1), (1, 2), (-1, 2), (-2, 1)]

# --- 1. 畫棋盤 ---
def draw_board(n):
    """畫出 n x n 的棋盤，每格交錯黑白顏色"""
    size = 600 / n          # 每格寬度（整個棋盤為 600px 寬）
    origin = -300           # 將棋盤置中（左下角為原點）
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)            # 畫筆速度最快

    # 逐格繪製棋盤
    for y in range(n):
        for x in range(n):
            px = origin + x * size
            py = origin + y * size
            pen.penup()
            pen.goto(px, py)
            color = "white" if (x + y) % 2 == 0 else "gray"  # 黑白交錯
            pen.fillcolor(color)
            pen.begin_fill()
            pen.pendown()
            for _ in range(4):
                pen.forward(size)
                pen.left(90)
            pen.end_fill()

# --- 2. 放置騎士 ---
def place_knight(x, y, n):
    """將騎士放在棋盤上 (x, y) 格子的中心位置"""
    size = 600 / n
    origin = -300
    px = origin + x * size + size / 2
    py = origin + y * size + size / 2

    knight = turtle.Turtle()
    knight.shape("circle")
    knight.color("blue")
    knight.penup()
    knight.goto(px, py)
    knight.stamp()  # 印出騎士形狀（不會移動）
    return knight

# --- 3. 使用 Warnsdorff 規則自動巡遊並動畫顯示 ---
def run_warnsdorff_animation(n, start_x, start_y):
    """騎士根據 Warnsdorff 演算法，自動跳遍棋盤，並動畫顯示每一步"""
    board = [[0] * n for _ in range(n)]  # 棋盤紀錄，0 代表尚未拜訪
    x, y = start_x, start_y
    size = 600 / n
    origin = -300

    # 騎士物件
    knight = turtle.Turtle()
    knight.shape("circle")
    knight.color("blue")
    knight.penup()
    knight.speed(1)

    # 寫步數用的筆
    writer = turtle.Turtle()
    writer.hideturtle()
    writer.penup()
    writer.color("black")

    # 開始巡遊
    for step in range(1, n * n + 1):
        board[y][x] = step

        # 畫出騎士與步數
        px = origin + x * size + size / 2
        py = origin + y * size + size / 2
        knight.goto(px, py)
        knight.stamp()
        writer.goto(px, py - size / 4)
        writer.write(str(step), align="center", font=("Arial", int(size / 5), "normal"))
        time.sleep(0.1)

        # 找出下一步可走位置，並根據 Warnsdorff 規則挑最少分支的
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
            break  # 沒有合法下一步，巡遊結束

        candidates.sort()
        _, x, y = candidates[0]  # 選擇選項數最少的格子

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

    # 2️⃣ 詢問起點位置選擇方式
    m = int(input("2.選擇起點：1 表示 (0,0)；2 表示隨機位置："))
    if m == 1:
        start_x, start_y = 0, 0
    else:
        start_x = random.randint(0, n - 1)
        start_y = random.randint(0, n - 1)

    print(f"✅ 起點位置為：({start_x}, {start_y})")

    # 3️⃣ 初始化畫面與執行繪圖與動畫
    turtle.setup(700, 700)
    turtle.title(f"{n}x{n} 騎士巡遊動畫 - Warnsdorff")
    turtle.tracer(0)  # 先不立即更新畫面，加速畫棋盤
    draw_board(n)
    turtle.update()  # 一次更新畫面
    run_warnsdorff_animation(n, start_x, start_y)
    turtle.done()

main()
