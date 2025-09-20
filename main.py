# main.py

from tkinter import *
import ground
import movement
import game_state
import character
import menu_ui 
import game_controller 

# Import các biến config 
from config import WIDTH, HEIGHT, do_dai, toc_do


# ------------------ Khởi tạo Tkinter và Canvas ------------------
root = Tk()
root.title("Snake Game CS101")

# Gán các biến config vào game_state
game_state.WIDTH = WIDTH
game_state.HEIGHT = HEIGHT
game_state.do_dai = do_dai
game_state.toc_do = toc_do

# Gán canvas vào game_state
canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()
game_state.canvas = canvas


# ------------------ Khởi tạo Game ------------------
# 1. Vẽ nền lưới 
# Vùng chơi:
game_state.Pos_apple=ground.ground(canvas, WIDTH, HEIGHT, do_dai, do_dai*2, WIDTH-do_dai, HEIGHT-do_dai, do_dai, "#AAD751", "#A2D149")

# [THAY ĐỔI] Gán phím điều khiển ngay từ đầu (nhưng logic sẽ chặn nó hoạt động)
movement.bind_keys(root)
menu_ui.keys_bound = True # Đặt True để menu_ui không gán lại

# 2. Load tất cả ảnh (Skins, Menu, Buttons)
menu_ui.load_menu_assets(root, canvas, do_dai)

# 3. Hiển thị Menu ban đầu
menu_ui.draw_menu()

# 4. Chạy vòng lặp chính của Tkinter
root.mainloop()