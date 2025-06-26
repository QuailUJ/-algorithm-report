import turtle

# --- 1. 畫棋盤函式 ---
def draw_board(n):
    """繪製 n x n 棋盤，使用黑白交錯方格"""
    size = 600 / n           # 每格大小，整體棋盤寬度為 600 px
    origin = -300            # 左下角起點座標，使棋盤置中
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

# --- 2. 放置棋子函式 ---
def place_knight(x, y, n):
    """將棋子放在 (x, y) 格子中央，棋盤大小為 n x n"""
    size = 600 / n
    origin = -300
    px = origin + x * size + size / 2
    py = origin + y * size + size / 2

    knight = turtle.Turtle()
    knight.shape("circle")   
    knight.color("blue")
    knight.penup()
    knight.goto(px, py)
    knight.stamp()           # 留下圖章表示棋子位置（可移除）

# --- 主程式 ---
def main():
    n = int(input("請輸入想要格數:"))  # 棋盤大小
    knight = place_knight(0, 0, n)  # 騎士預設在左下角 (0, 0)
    turtle.setup(700, 700)
    turtle.title(f"{n}x{n} 騎士棋盤")
    turtle.tracer(0)        # 關掉動畫效果，加速畫面繪製
    draw_board(n)
    place_knight(0, 0, n)   # 將棋子放在左下角 (0,0)
    turtle.update()
    turtle.done()

    

main()
