from pico2d import load_image, get_canvas_width, get_canvas_height


# ---- 스프라이트 ----
FRAME_W, FRAME_H = 88, 80                 # horong_sheet.png 한 칸 크기 (4칸: 대기, 걷기1~3)
DRAW_W, DRAW_H = 66, 60                   # 화면에 그릴 크기


class Player:
    def __init__(self):
        self.x, self.y = get_canvas_width() // 2, get_canvas_height() // 2
        self.image = load_image('resource/horong_sheet.png')
        self.frame = 0

    # ---- 매 프레임 ----
    def update(self):
        pass

    def draw_frame(self, index):
        self.image.clip_draw(index * FRAME_W, 0, FRAME_W, FRAME_H, self.x, self.y, DRAW_W, DRAW_H)

    def draw(self):
        self.draw_frame(0)
