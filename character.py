# character.py

from PIL import Image, ImageTk 
from config import *

# Khai báo skins để dễ bảo trì
skins = {}

# Định nghĩa hàm tải skin
def load_skin(path="Asset/main/character/", size=(do_dai, do_dai)):
    def load_img(filename):

        return Image.open(f"{path}{filename}").resize(size, Image.LANCZOS)

    return {
        "head": {
            "right": load_img("head_right.png"),
            "down":  load_img("head_down.png"),
            "left":  load_img("head_left.png"),
            "up":    load_img("head_up.png"),
        },
        "body": {
            "bottomleft":  load_img("body_bottomleft.png"),
            "bottomright": load_img("body_bottomright.png"),
            "topright":    load_img("body_topright.png"),
            "topleft":     load_img("body_topleft.png"),
            "horizontal":  load_img("body_horizontal.png"),
            "vertical":    load_img("body_vertical.png"),
        },
        "tail": {
            "down":  load_img("tail_down.png"),
            "up":    load_img("tail_up.png"),
            "right": load_img("tail_right.png"),
            "left":  load_img("tail_left.png"),
        },
        "apple": load_img("apple.png")
    }

def initialize_skins():
    global skins
    if not skins:
        skins["main"] = load_skin("asset/main/character/", size=(do_dai, do_dai))

def get_photoimage(img):
    return ImageTk.PhotoImage(img)

Image = Image
ImageTk = ImageTk

#triệu hồi rắn =))
def spawn_snake(start_x=6, start_y=9, length=3, direction="right"):
    snake_coords = []
    # Xác định hướng ban đầu
    if direction == "right":
        dx, dy = -1, 0  # trái
    elif direction == "left":
        dx, dy = 1, 0   # phải
    elif direction == "up":
        dx, dy = 0, 1   #  xuống
    elif direction == "down":
        dx, dy = 0, -1  # lên
    else:
        dx, dy = 0, 0 # không di chuyển =))

    # Tạo tọa độ từng phần body
    for i in range(length):
        x = start_x + i * dx
        y = start_y + i * dy
        snake_coords.append((x, y))
        
    return snake_coords