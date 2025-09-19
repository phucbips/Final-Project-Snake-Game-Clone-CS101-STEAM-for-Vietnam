import game_state
import movement
import character
import menu_ui
import random
import config


def spawn_food(random_spawn=True):
    canvas = game_state.canvas
    do_dai = config.do_dai
    grid_width = game_state.WIDTH // do_dai
    grid_height = game_state.HEIGHT // do_dai

    if not game_state.snake_coords:
        random_spawn = True

    if random_spawn:
        # Logic cho vị trí ngẫu nhiên
        while True:
            fx,fy=random.choice(game_state.Pos_apple)
            new_food_coord = (fx/do_dai, fy/do_dai)
            if new_food_coord not in game_state.snake_coords:
                break
    else:

        head_x, head_y = game_state.snake_coords[0]
        if head_x + 4 < grid_width:
            fx, fy = head_x + 4, head_y
        elif head_x - 4 >= 0:
            fx, fy = head_x - 4, head_y

        new_food_coord = (fx, fy)

    # Xoá food cũ
    if game_state.food_item:
        canvas.delete(game_state.food_item)

    # Lưu tọa độ logic của food
    game_state.food_coord = new_food_coord

    # Chuyển đổi tọa độ logic
    fx_pixel, fy_pixel = new_food_coord[0] * do_dai, new_food_coord[1] * do_dai

    # Vẽ food mới
    game_state.food_item = canvas.create_image(
        fx_pixel, fy_pixel,
        image=menu_ui.apple_img,
        anchor="nw",
        tags="food"
    )


def check_eat_food():
    """Kiểm tra xem đầu rắn có trùng với tọa độ food không."""
    if not game_state.snake_coords or not game_state.food_coord:
        return False
    return game_state.snake_coords[0] == game_state.food_coord


def update_score():
    canvas = game_state.canvas
    canvas.delete("score_display")
    menu_ui.draw_scoreboard()


def game_loop():
    canvas = game_state.canvas

    if game_state.GAME_OVER:
        menu_ui.game_over_screen()
        return

    if not game_state.GAME_PAUSED:
        grow = check_eat_food()
        if grow:
            game_state.SCORE += 1
            update_score()
            # Spawn táo
            spawn_food(random_spawn=True)

        move_success = movement.move_snake(character.skins["main"], grow=grow)

        if not move_success:
            game_state.GAME_OVER = True
            canvas.delete("score_display")
            canvas.delete("snake")
            canvas.delete("food")

    canvas.after(game_state.toc_do, game_loop)


def start_game():
    canvas = game_state.canvas
    #xóa menu cũ
    canvas.delete("menu")

    # Thiết lập trạng thái game
    movement.current_dir = "right"
    game_state.SCORE = 0
    game_state.GAME_OVER = False
    game_state.GAME_PAUSED = True
    game_state.snake_parts = []

    # 1. Khởi tạo rắn
    start_x, start_y = 6, 9
    game_state.snake_coords = character.spawn_snake(start_x, start_y, length=3, direction=movement.current_dir)
    movement._redraw_snake(character.skins["main"])

    # 2. Spawn food lần đầu
    spawn_food(random_spawn=False)

    # 3. Vẽ Scoreboard
    update_score()

    # 4. Bắt đầu game loop
    game_loop()
