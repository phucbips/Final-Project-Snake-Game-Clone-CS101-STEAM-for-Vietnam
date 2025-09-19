from config import WIDTH, HEIGHT
import game_state
import character
from tkinter import messagebox
import game_controller
import ground  # Cần để vẽ lại nền trong Game Over
import movement  # Import movement module để bind key
import os  # Cần để kiểm tra file có tồn tại không

# Các biến cần thiết để vẽ menu (biến global)
menu1_img = None
frames = []
apple_img = None
apple_score_img = None
trophy_img = None
keys_bound = False


# --- LOAD ASSETS ---
def load_menu_assets(root, canvas, do_dai):
    """Tải tất cả ảnh cần thiết cho Menu, Táo và Scoreboard."""
    global menu1_img, frames, apple_img, apple_score_img, trophy_img

    # 1. Khởi tạo Skins (chứa cả ảnh táo game)
    character.initialize_skins()

    # 2. Đọc High Score từ file
    if os.path.exists('highscore.txt'):
        try:
            with open('highscore.txt', 'r') as file:
                game_state.HIGH_SCORE = int(file.read())
        except (ValueError, FileNotFoundError):
            game_state.HIGH_SCORE = 0
    else:
        game_state.HIGH_SCORE = 0

    try:
        # 3. Cắt ảnh menu1
        menu1_img_pil = character.Image.open("Asset/menu/menu1.png")
        menu1_img_pil = menu1_img_pil.crop((693, 1, 842, 149))
        menu1_img_pil = menu1_img_pil.resize((301, 354), character.Image.LANCZOS)
        menu1_img = character.ImageTk.PhotoImage(menu1_img_pil)

        # 4. Cắt ảnh button
        sprite_sheet = character.Image.open("Asset/menu/button.png")
        for i in range(5):
            x1 = 61 + i * 257
            y1 = 49
            x2 = 196 + i * 257
            y2 = 124
            frame = sprite_sheet.crop((x1, y1, x2, y2))
            frame = frame.resize((301, 125), character.Image.LANCZOS)
            frames.append(character.ImageTk.PhotoImage(frame))

        # 5. Ảnh Táo game (40x40)
        apple_img = character.get_photoimage(
            character.skins["main"]["apple"].resize((do_dai, do_dai), character.Image.LANCZOS))

        # 6. Ảnh Táo scoreboard (30x30)
        apple_score_img = character.get_photoimage(
            character.skins["main"]["apple"].resize((30, 30), character.Image.LANCZOS))

        # 7. Ảnh Trophy (30x30)
        trophy_img_pil = character.Image.open("Asset/main/character/trophy.png").resize((30, 30),
                                                                                        character.Image.LANCZOS)
        trophy_img = character.ImageTk.PhotoImage(trophy_img_pil)

    except FileNotFoundError as e:
        print(f"Lỗi: Không tìm thấy file ảnh! Vui lòng kiểm tra thư mục 'asset' và các file ảnh: {e}")
        exit()


# --- SCOREBOARD ---
def draw_scoreboard(anchor_x=40, anchor_y=40):
    """Vẽ Scoreboard (Current Score & High Score) lên góc trên bên trái."""
    canvas = game_state.canvas
    W = game_state.WIDTH
    H = game_state.HEIGHT

    # Cập nhật High Score
    if game_state.SCORE > game_state.HIGH_SCORE:
        game_state.HIGH_SCORE = game_state.SCORE

    # Vị trí cho Scoreboard (cố định ở góc trái trên)

    # --- Hiển thị Current Score (Apple) ---
    canvas.create_image(
        anchor_x, anchor_y,
        image=apple_score_img,
        tags="score_display",
        anchor="center"
    )
    canvas.create_text(
        anchor_x + 30, anchor_y,
        text=f"{game_state.SCORE}",
        fill="white",
        font=("Consolas", 30, "bold"),
        anchor="w",
        tags="score_display"
    )

    # --- Hiển thị High Score (Trophy) ---
    canvas.create_image(
        anchor_x + 110, anchor_y,
        image=trophy_img,
        tags="score_display",
        anchor="center"
    )
    canvas.create_text(
        anchor_x + 140, anchor_y,
        text=f"{game_state.HIGH_SCORE}",
        fill="yellow",
        font=("Consolas", 30, "bold"),
        anchor="w",
        tags="score_display"
    )

def animation_button(tag_name, index=0):
    canvas = game_state.canvas

    if canvas.find_withtag("menu"):
        canvas.itemconfig(tag_name, image=frames[index])
        next_index = (index + 1) % len(frames)
        # Lặp lại animation sau 150ms
        canvas.after(150, animation_button, tag_name, next_index)


def draw_menu():
    """Vẽ màn hình Menu chính."""
    canvas = game_state.canvas
    W = game_state.WIDTH
    H = game_state.HEIGHT

    ground.ground(canvas, W, H, game_state.do_dai, game_state.do_dai * 2, W - game_state.do_dai, H - game_state.do_dai,
                  game_state.do_dai, "#AAD751", "#A2D149")

    # Background mờ
    canvas.create_rectangle(0, 0, W, H, fill="#000000", stipple="gray75", tags="menu")

    # Logo/Tiêu đề
    canvas.create_image(W / 2, H / 2 - 40, image=menu1_img, tags="menu")

    #Nút Start
    button_x = W / 2
    button_y = H / 2 + 240

    canvas.button_image_ref = frames[0]

    canvas.create_image(
        button_x,
        button_y,
        image=frames[0],
        tags=("menu", "start_button")
    )

    canvas.tag_bind("start_button", "<Button-1>", on_click_button_start)
    animation_button("start_button")


def on_click_button_start(event):
    global keys_bound
    canvas = game_state.canvas

    print("Bắt đầu trò chơi...")
    canvas.delete("menu")  # Xóa toàn bộ menu

    # Lấy cửa sổ gốc
    root = canvas.winfo_toplevel()

    game_controller.start_game()
    game_state.start_game = True

    if not keys_bound:
        movement.bind_keys(root)
        keys_bound = True

def game_over_screen():
    """Hiển thị màn hình Game Over và gọi lại Menu"""
    W = game_state.WIDTH
    H = game_state.HEIGHT
    canvas = game_state.canvas

    # Cập nhật High Score
    if game_state.SCORE > game_state.HIGH_SCORE:
        game_state.HIGH_SCORE = game_state.SCORE
        # lưu high score vào file
    try:
        with open('highscore.txt', 'w') as file:
            file.write(str(game_state.HIGH_SCORE))
    except IOError as e:
        print(f"Lỗi khi ghi file highscore.txt: {e}")

    global keys_bound
    keys_bound = False

    # Xóa tất cả và vẽ lại nền
    canvas.delete("all")
    ground.ground(canvas, W, H, game_state.do_dai, game_state.do_dai * 2, W - game_state.do_dai, H - game_state.do_dai,
                  game_state.do_dai, "#AAD751", "#A2D149")
    draw_menu()
    draw_scoreboard(310, 160)
