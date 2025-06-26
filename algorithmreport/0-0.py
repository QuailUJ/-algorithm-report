# 演示回朔法
import turtle
import time

# 騎士可跳的方向（8 種 L 型移動）
moves = [(-2, -1), (-1, -2), (1, -2), (2, -1),
         (2, 1), (1, 2), (-1, 2), (-2, 1)]

# 棋盤顯示總寬度（像素）
BOARD_PIXEL_WIDTH = 600

# --- 0️⃣ 輔助：將單一格子重新填回原本顏色 ---
def fill_square(x, y, n):
    """
    將 (x, y) 格子重新填滿原本顏色（黑白交錯）。
    使用臨時 Turtle 完成填色後立即清除，以免留下多餘物件。
    """
    size = BOARD_PIXEL_WIDTH / n
    origin = -BOARD_PIXEL_WIDTH / 2
    px = origin + x * size
    py = origin + y * size
    filler = turtle.Turtle()
    filler.hideturtle()
    filler.speed(0)
    filler.penup()
    filler.goto(px, py)
    color = "white" if (x + y) % 2 == 0 else "gray"
    filler.fillcolor(color)
    filler.begin_fill()
    filler.pendown()
    for _ in range(4):
        filler.forward(size)
        filler.left(90)
    filler.end_fill()
    filler.penup()
    filler.clear()  # 清除填色用的 Turtle

# --- 1️⃣ 畫棋盤 ---
def draw_board(n):
    """畫出 n x n 的棋盤，黑白格子交錯填滿視窗"""
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

# --- 2️⃣ 放置騎士 ---
def place_knight(x, y, n):
    """在 (x, y) 格子的中心位置放置騎士並回傳此 Turtle 物件"""
    size = BOARD_PIXEL_WIDTH / n
    origin = -BOARD_PIXEL_WIDTH / 2
    px = origin + x * size + size / 2
    py = origin + y * size + size / 2
    knight = turtle.Turtle()
    knight.shape("circle")
    knight.shapesize(1.5, 1.5, 1.5)
    knight.color("blue")
    knight.penup()
    knight.speed(1)  # 瞬間移動
    knight.goto(px, py)
    knight.stamp()
    return knight

# --- 3️⃣ 自動回溯法 + 畫面動畫顯示（含候選分支列出） ---
def knight_tour_auto(n, board, path, step, knight, num_writers, stamps, visited_paths, start_time):
    """
    自動回溯尋找騎士巡遊；每步自動依序嘗試所有候選分支，並在終端列印：
      - 「目前位置」與「可行路線清單」
    回溯時：
      - 恢復格子顏色
      - 刪除數字與圖章
    找到完整路徑後，會印出耗時。
    參數：
      - board: 2D list，0 表示未訪問，非 0 為已訪問步數
      - path: list of (x, y)，紀錄目前路徑
      - step: 已訪問格子數（起點為 1）
      - knight: 放騎士的 Turtle
      - num_writers: list of Turtle，用於顯示每步步數
      - stamps: list of stamp id，用於回溯時刪除 stamp
      - visited_paths: set，儲存所有死路路徑
      - start_time: float，開始計時的時間戳記
    """
    # 若已拜訪所有 n*n 格子，完成巡遊
    if step == n * n:
        elapsed = time.time() - start_time
        print(f"✅ 自動找到完整巡遊！花費時間: {elapsed:.2f} 秒")
        return True

    x, y = path[-1]
    size = BOARD_PIXEL_WIDTH / n
    origin = -BOARD_PIXEL_WIDTH / 2

    # 計算所有可行分支
    candidates = []
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n and board[ny][nx] == 0:
            candidates.append((nx, ny))

    # 列印目前位置與候選分支
    print(f"🔹 步數 {step}，目前位置：({x}, {y})")
    print(f"   可行路線共 {len(candidates)} 條，分別為：{candidates}")

    # 若無可行分支，記錄死路並回溯
    if not candidates:
        visited_paths.add(tuple(path))
        print(f"⚠️ 死路，記錄此路徑：{path}")
        return False

    # 依序嘗試
    for nx, ny in candidates:
        potential = tuple(path + [(nx, ny)])
        skip = False
        for dead in visited_paths:
            if len(potential) <= len(dead) and potential == dead[: len(potential)]:
                skip = True
                break
        if skip:
            continue

        # 標記下一步
        board[ny][nx] = step + 1
        path.append((nx, ny))

        # 畫騎士移動與步數
        px = origin + nx * size + size / 2
        py = origin + ny * size + size / 2

        knight.goto(px, py)
        stamp_id = knight.stamp()
        stamps.append(stamp_id)

        num_turtle = turtle.Turtle()
        num_turtle.hideturtle()
        num_turtle.penup()
        num_turtle.color("red")
        num_turtle.goto(px, py - size / 4)
        num_turtle.write(str(step + 1), align="center", font=("Arial", int(size / 5), "normal"))
        num_writers.append(num_turtle)

        time.sleep(0.1)    # 若要更快，可改成更小或註解掉
        turtle.update()      # 手動更新畫面

        # 遞迴嘗試
        if knight_tour_auto(n, board, path, step + 1, knight, num_writers, stamps, visited_paths, start_time):
            return True

        # 回溯：刪除畫面上剛畫的內容，並恢復格子顏色
        board[ny][nx] = 0
        path.pop()

        writer_turtle = num_writers.pop()
        writer_turtle.clear()
        writer_turtle.hideturtle()
        writer_turtle.clear()

        knight.clearstamp(stamps.pop())

        fill_square(nx, ny, n)
        turtle.update()

    return False

# --- 4️⃣ 重播正確路徑動畫 ---
def animate_solution(n, path):
    """當找到完整路徑後，清空畫面並用動畫再次展示該路徑"""
    size = BOARD_PIXEL_WIDTH / n
    origin = -BOARD_PIXEL_WIDTH / 2

    turtle.clearscreen()            # 清空畫面，但保留 Turtle 環境
    screen = turtle.Screen()
    screen.setup(BOARD_PIXEL_WIDTH, BOARD_PIXEL_WIDTH)
    screen.title(f"{n}x{n} 騎士巡遊 - 正確路徑重播")
    screen.tracer(0)

    draw_board(n)
    turtle.update()

    knight = turtle.Turtle()
    knight.shape("circle")
    knight.shapesize(1.5, 1.5, 1.5)
    knight.color("blue")
    knight.penup()
    knight.speed(1)

    writer = turtle.Turtle()
    writer.hideturtle()
    writer.penup()
    writer.color("red")

    for step, (x, y) in enumerate(path, start=1):
        px = origin + x * size + size / 2
        py = origin + y * size + size / 2
        knight.goto(px, py)
        knight.stamp()
        writer.goto(px, py - size / 4)
        writer.write(str(step), align="center", font=("Arial", int(size / 5), "normal"))
        time.sleep(0.1)
        turtle.update()

# --- 5️⃣ 主程式 ---
def main():
    # 1. 輸入棋盤大小
    while True:
        try:
            n = int(input("請輸入棋盤邊長 n（>=1）："))
            if n >= 1:
                break
            print("請輸入大於等於 1 的整數")
        except ValueError:
            print("格式錯誤，請再輸入一次")

    # 2. 初始化視窗與棋盤
    turtle.setup(BOARD_PIXEL_WIDTH, BOARD_PIXEL_WIDTH)
    turtle.title(f"{n}x{n} 騎士巡遊")
    turtle.tracer(0)
    draw_board(n)
    turtle.update()

    # 3. 初始化棋盤資料與路徑
    board = [[0] * n for _ in range(n)]
    start_x, start_y = 0, 0
    board[start_y][start_x] = 1
    path = [(start_x, start_y)]
    visited_paths = set()

    # 4. 放置騎士在起始格，並顯示「1」
    knight = place_knight(start_x, start_y, n)
    size = BOARD_PIXEL_WIDTH / n
    origin = -BOARD_PIXEL_WIDTH / 2
    px0 = origin + start_x * size + size / 2
    py0 = origin + start_y * size + size / 2
    writer0 = turtle.Turtle()
    writer0.hideturtle()
    writer0.penup()
    writer0.color("red")
    writer0.goto(px0, py0 - size / 4)
    writer0.write("1", align="center", font=("Arial", int(size / 5), "normal"))
    num_writers = [writer0]

    # 5. 初始化圖章 ID 列表（包含起點 stamp）
    stamps = [knight.stamp()]

    # 6. 開始計時
    start_time = time.time()

    # 7. 啟動自動回溯搜尋
    found = knight_tour_auto(n, board, path, 1, knight, num_writers, stamps, visited_paths, start_time)

    if not found:
        print("⚠️ 無解！")
        turtle.done()
        return

    # 8. 找到完整路徑後，重播正確路徑
    time.sleep(0.5)
    animate_solution(n, path)

    turtle.done()

main()
