import turtle
import time

# 騎士可跳的方向（8 種 L 型移動）
moves = [(-2, -1), (-1, -2), (1, -2), (2, -1),
         (2, 1), (1, 2), (-1, 2), (-2, 1)]

# 棋盤顯示總寬度（像素）
BOARD_PIXEL_WIDTH = 600

# --- 輔助：將單一格子重新填回原本顏色 ---
def fill_square(x, y, n):
    """
    將 (x, y) 格子重新填滿原本顏色（黑白交錯）。
    不留下額外 turtle 物件。
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
    filler.clear()  # 刪除畫填充用的 turtle

# --- 1️⃣ 畫棋盤 ---
def draw_board(n):
    """畫出 n x n 棋盤，黑白格子交錯"""
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
    """在 (x, y) 格子的中心位置放置騎士並回傳騎士物件"""
    size = BOARD_PIXEL_WIDTH / n
    origin = -BOARD_PIXEL_WIDTH / 2
    px = origin + x * size + size / 2
    py = origin + y * size + size / 2
    knight = turtle.Turtle()
    knight.shape("circle")
    knight.shapesize(1.5, 1.5, 1.5)
    knight.color("blue")
    knight.penup()
    knight.goto(px, py)
    knight.stamp()
    return knight

# --- 3️⃣ 主程式：手動操作並具備回溯功能 ---
def main():
    # 1. 讀取棋盤大小
    while True:
        try:
            n = int(input("請輸入棋盤邊長 n（>=1）："))
            if n >= 1:
                break
            print("請輸入大於等於 1 的整數")
        except ValueError:
            print("請輸入合法整數")

    # 2. 初始化視窗與棋盤
    turtle.setup(BOARD_PIXEL_WIDTH, BOARD_PIXEL_WIDTH)
    turtle.title(f"{n}x{n} 騎士巡遊 - 手動操作 + 回溯")
    turtle.tracer(0)
    draw_board(n)
    turtle.update()

    # 3. 初始化棋盤資料結構與路徑
    board = [[0] * n for _ in range(n)]
    start_x, start_y = 0, 0  # 起始格 (0,0)
    board[start_y][start_x] = 1
    path = [(start_x, start_y)]  # 存放已走路徑
    visited_paths = set()        # 紀錄死路路徑（不重複）

    # 4. 放置騎士在起始位置，並顯示步數 1
    knight = place_knight(start_x, start_y, n)
    num_writers = []
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
    num_writers.append(writer0)

    stamps = [knight.stamp()]  # 騎士的第一個 stamp ID

    step = 1  # 當前步數

    # 5. 主迴圈：讓使用者手動輸入下一步或自動回溯
    while True:
        x, y = path[-1]
        # 計算可行下一步
        candidates = []
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and board[ny][nx] == 0:
                candidates.append((nx, ny))

        if candidates:
            # 顯示可行分支
            print(f"步數 {step}，目前在 ({x}, {y})，可行分支：{candidates}")
            # 提示用戶輸入下一步
            while True:
                try:
                    user_input = input(f"請輸入下一步座標（格式: x y），或輸入 B 進行回溯：")
                    if user_input.strip().upper() == "B":
                        # 使用者要求回溯
                        nx, ny = None, None
                        break
                    parts = user_input.split(" ")
                    nx, ny = int(parts[0]), int(parts[1])
                    if (nx, ny) in candidates:
                        break
                    print("輸入座標不在可行分支裡，請重新輸入")
                except:
                    print("格式錯誤，請輸入 x y 或 B")

            # 如果使用者選擇回溯
            if nx is None and ny is None:
                if step == 1:
                    print("已回到起點，無法再回溯。")
                    continue
                # 執行回溯到上一步
                bx, by = path.pop()  # 移除當前格
                board[by][bx] = 0    # 清除棋盤標記
                # 刪除步數文字
                writer_turtle = num_writers.pop()
                writer_turtle.clear()
                writer_turtle.hideturtle()
                writer_turtle.clear()
                # 刪除騎士圖章
                knight.clearstamp(stamps.pop())
                # 塗回原本格色
                fill_square(bx, by, n)
                step -= 1
                print(f"回溯到步數 {step}，位置 {path[-1]}")
                continue

            # 使用者選擇了一條合法分支
            board[ny][nx] = step + 1
            path.append((nx, ny))
            step += 1

            # 騎士移動並 stamp
            px = origin + nx * size + size / 2
            py = origin + ny * size + size / 2
            knight.goto(px, py)
            stamp_id = knight.stamp()
            stamps.append(stamp_id)

            # 寫步數
            num_turtle = turtle.Turtle()
            num_turtle.hideturtle()
            num_turtle.penup()
            num_turtle.color("red")
            num_turtle.goto(px, py - size / 4)
            num_turtle.write(str(step), align="center", font=("Arial", int(size / 5), "normal"))
            num_writers.append(num_turtle)

            time.sleep(0.05)

            # 如果已走完所有格子，結束
            if step == n * n:
                print("🎉 已完成騎士巡遊！")
                break

        else:
            # 無可行分支，自動回溯
            print(f"⚠️ 無可行分支，步數 {step}，自動回溯")
            if step == 1:
                print("無法再回溯，遊戲結束")
                break
            bx, by = path.pop()
            board[by][bx] = 0
            # 刪除步數文字
            writer_turtle = num_writers.pop()
            writer_turtle.clear()
            writer_turtle.hideturtle()
            writer_turtle.clear()
            # 刪除騎士 stamp
            knight.clearstamp(stamps.pop())
            # 塗回原本顏色
            fill_square(bx, by, n)
            step -= 1
            print(f"回溯到步數 {step}，位置 {path[-1]}")

    print("最終路徑：", path)
    turtle.done()

main()
