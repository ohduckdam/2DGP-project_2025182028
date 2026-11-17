from pico2d import load_image, get_canvas_height

from player import MAX_OIL

BAR_LEFT, BAR_TOP = 24, 24            # 화면 왼쪽 위에서 떨어진 거리
BACK_W, BACK_H = 204, 20
FILL_W, FILL_H = 200, 16


class OilGauge:
    """왼쪽 위 기름 게이지 (기름 = 체력)"""

    def __init__(self, player):
        self.player = player
        self.back = load_image('resource/oil_bar_back.png')
        self.fill = load_image('resource/oil_bar_fill.png')

    def update(self):
        pass

    def draw(self):
        cy = get_canvas_height() - BAR_TOP - BACK_H / 2
        self.back.draw(BAR_LEFT + BACK_W / 2, cy)
        w = int(FILL_W * self.player.oil / MAX_OIL)
        if w > 0:
            # 남은 기름 비율만큼만 잘라서 왼쪽부터 그린다
            self.fill.clip_draw(0, 0, w, FILL_H, BAR_LEFT + 2 + w / 2, cy)
