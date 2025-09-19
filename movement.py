from turtledemo.penrose import start
import character
import game_state
import movement
import config

# Hướng: (dx, dy)
directions = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}
current_dir = "right"  # hướng ban đầu


def set_direction(new_dir):
    global current_dir
    if not game_state.DIRECTION_LOCKED:
        dx, dy = directions[current_dir]
        ndx, ndy = directions[new_dir]
        if (dx + ndx, dy + ndy) != (0, 0):  # không cho quay ngược
            current_dir = new_dir
            game_state.DIRECTION_LOCKED = True  # Khóa hướng ngay sau khi đổi

            if game_state.GAME_PAUSED:
                game_state.GAME_PAUSED = False


def bind_keys(root):
    """Gán phím điều khiển."""

    root.bind("<Up>", lambda e: set_direction("up"))
    root.bind("<Down>", lambda e: set_direction("down"))
    root.bind("<Left>", lambda e: set_direction("left"))
    root.bind("<Right>", lambda e: set_direction("right"))
    root.bind("w", lambda e: set_direction("up"))
    root.bind("s", lambda e: set_direction("down"))
    root.bind("a", lambda e: set_direction("left"))
    root.bind("d", lambda e: set_direction("right"))


def _get_direction(p1, p2):
    """Tính hướng di chuyển từ p1 đến p2."""
    if p2[0] > p1[0]: return "right"
    if p2[0] < p1[0]: return "left"
    if p2[1] > p1[1]: return "down"
    if p2[1] < p1[1]: return "up"
    return None


def _redraw_snake(skin):
    canvas = game_state.canvas
    do_dai = game_state.do_dai
    snake_coords = game_state.snake_coords

    # Xóa các đối tượng rắn cũ
    canvas.delete("snake")
    game_state.snake_parts = []
    new_image_refs = []

    for i, (x, y) in enumerate(snake_coords):
        img_pil = None

        # 1. đầu
        if i == 0:
            img_pil = skin["head"][current_dir]

        # 2. đuôi
        elif i == len(snake_coords) - 1:
            px2, py2 = snake_coords[-2]
            tail_dir = _get_direction((px2, py2), (x, y))
            img_pil = skin["tail"][tail_dir]

        # 3. thân
        else:
            prev = snake_coords[i - 1]
            nxt = snake_coords[i + 1]

            # Trường hợp thẳng: Thân dọc
            if prev[0] == nxt[0]:
                img_pil = skin["body"]["vertical"]
            elif prev[1] == nxt[1]:
                img_pil = skin["body"]["horizontal"]

            # Trường hợp cong (góc)
            else:

                # TopLeft: prev/nxt ở (trái, trên)
                if ((prev[0] < x and nxt[1] < y) or (nxt[0] < x and prev[1] < y)):
                    key = "topleft"
                # BottomLeft: prev/nxt ở (trái, dưới)
                elif ((prev[0] < x and nxt[1] > y) or (nxt[0] < x and prev[1] > y)):
                    key = "bottomleft"
                # TopRight: prev/nxt ở (phải, trên)
                elif ((prev[0] > x and nxt[1] < y) or (nxt[0] > x and prev[1] < y)):
                    key = "topright"
                # BottomRight: prev/nxt ở (phải, dưới)
                elif ((prev[0] > x and nxt[1] > y) or (nxt[0] > x and prev[1] > y)):
                    key = "bottomright"
                else:
                    key = "horizontal"

                img_pil = skin["body"][key]

        img = character.get_photoimage(img_pil.resize((do_dai, do_dai)))
        new_image_refs.append(img)

        part_id = canvas.create_image(
            x * do_dai, y * do_dai,
            image=img,
            anchor="nw",
            tags="snake"
        )
        game_state.snake_parts.append(part_id)

    canvas.image_ref = new_image_refs


def move_snake(skin, grow=False):
    """Tính toán tọa độ rắn mới và kiểm tra va chạm. Trả về True nếu di chuyển thành công."""
    canvas = game_state.canvas
    do_dai = game_state.do_dai

    head_x, head_y = game_state.snake_coords[0]
    dx, dy = directions[current_dir]
    new_head_x, new_head_y = head_x + dx, head_y + dy
    grid_width = game_state.WIDTH // do_dai
    grid_height = game_state.HEIGHT // do_dai

    # Ranh giới của sân chơi
    min_x = 1
    min_y = 2
    max_x = grid_width - 2
    max_y = grid_height - 2

    # Kiểm tra va chạm với tường mới
    if not (min_x <= new_head_x <= max_x and min_y <= new_head_y <= max_y):
        return False  # Game Over

    body_coords_to_check = game_state.snake_coords[:-1]
    if new_head_x == game_state.snake_coords[1][0] and new_head_y == game_state.snake_coords[1][1] and len(
            game_state.snake_coords) > 1 and not grow:
        pass
    elif (new_head_x, new_head_y) in body_coords_to_check:
        return False

    game_state.snake_coords.insert(0, (new_head_x, new_head_y))

    if not grow:
        game_state.snake_coords.pop()
    _redraw_snake(skin)
    game_state.DIRECTION_LOCKED = False
    return True
