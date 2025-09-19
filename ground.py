def ground(canvas, WIDTH, HEIGHT, x1, y1, x2, y2, do_dai, color1, color2):
    # Xóa nền cũ
    canvas.delete("ground")
    # Vẽ nền ngoài
    canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill='#6AB038', outline='#6AB038', tags="ground")
    pos_x = x1
    pos_y = y1
    # Tính số ô
    ngang = int((x2 - x1) / do_dai)
    doc = int((y2 - y1) / do_dai)
    Pos_apple = []
    # Vòng lặp vẽ bàn cờ =))
    for i in range(doc):
        pos_x = x1
        for j in range(ngang):
            if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                fill_color = color1 # Màu ô 1
            else:
                fill_color = color2 # Màu ô 2
            canvas.create_rectangle(
                pos_x, pos_y, pos_x + do_dai, pos_y + do_dai,
                fill=fill_color, outline=fill_color,
                tags="ground"
            )
            Pos_apple.append((pos_x, pos_y))
            pos_x += do_dai
        pos_y += do_dai
    return Pos_apple