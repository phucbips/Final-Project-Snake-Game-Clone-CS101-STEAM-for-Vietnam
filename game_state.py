# game_state.py

from tkinter import Canvas
import character # Import để dùng class Image

# Biến config (sẽ được gán giá trị từ main.py)
WIDTH: int = 0
HEIGHT: int = 0
do_dai: int = 0
toc_do: int = 0

# Biến Trạng thái Game
canvas: Canvas = None
score_label = None 

# Quản lý hướng di chuyển
DIRECTION_LOCKED = False 

# Danh sách chứa TỌA ĐỘ (x, y)
snake_coords = [] 
snake_parts = []

# Tọa độ và đối tượng của thức ăn
food_coord = None 
food_item = None 

# Điểm số và trạng thái
SCORE = 0
HIGH_SCORE = 0 
GAME_OVER = False
GAME_PAUSED = True

Pos_apple = []