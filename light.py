from pico2d import load_image, get_canvas_width, get_canvas_height

# tools/make_resources.py 의 값과 같아야 한다
SPREAD_SIZE = 512          # spread_hole.png 크기
SPREAD_BASE_R = 128        # spread_hole.png 의 기준 빛 반경

SPREAD_RADIUS = 240        # 빛 반경 (px)


class Light:
    """호롱의 등불 빛. 빛이 닿지 않는 곳을 어둠으로 덮는다. (game_world.DARKNESS 레이어)"""

    def __init__(self, player):
        self.player = player
        self.spread_hole = load_image('resource/spread_hole.png')
        self.dark = load_image('resource/dark.png')

    @property
    def radius(self):
        return SPREAD_RADIUS

    # ---- 그리기 ----
    def fill_outside(self, left, bottom, right, top):
        """화면에서 사각형 (left, bottom)~(right, top) 바깥을 모두 어둠으로 칠한다."""
        w, h = get_canvas_width(), get_canvas_height()
        left, right = max(0, int(left) + 1), min(w, int(right) - 1)      # 1px 겹치게 해서 틈이 생기지 않도록
        bottom, top = max(0, int(bottom) + 1), min(h, int(top) - 1)
        if left >= right or bottom >= top:                                 # 구멍이 화면 밖이면 전체를 덮는다
            self.dark.draw(w / 2, h / 2, w, h)
            return
        if left > 0:
            self.dark.draw(left / 2, h / 2, left, h)
        if right < w:
            self.dark.draw((right + w) / 2, h / 2, w - right, h)
        if bottom > 0:
            self.dark.draw((left + right) / 2, bottom / 2, right - left, bottom)
        if top < h:
            self.dark.draw((left + right) / 2, (top + h) / 2, right - left, h - top)

    def update(self):
        pass

    def draw(self):
        p = self.player
        size = SPREAD_SIZE * self.radius / SPREAD_BASE_R
        self.spread_hole.draw(p.x, p.y, size, size)
        half = size / 2
        self.fill_outside(p.x - half, p.y - half, p.x + half, p.y + half)
