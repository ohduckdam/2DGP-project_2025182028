import math

from pico2d import load_image, get_canvas_width, get_canvas_height
from sdl2 import (SDL_KEYDOWN, SDL_KEYUP, SDLK_w, SDLK_a, SDLK_s, SDLK_d)
from transitions import Machine

import game_framework

# ---- 수치 (기획서 기준, 나중에 밸런스 조정) ----
MOVE_SPEED = 200          # 이동 속도 (px/초)

# ---- 스프라이트 ----
FRAME_W, FRAME_H = 88, 80                 # horong_sheet.png 한 칸 크기 (4칸: 대기, 걷기1~3)
DRAW_W, DRAW_H = 66, 60                   # 화면에 그릴 크기
RUN_FRAMES = [1, 2, 3, 2]                 # 걷기 애니메이션 순서
RUN_FPS = 8                               # 걷기 애니메이션 초당 프레임

MOVE_KEYS = {SDLK_w: (0, 1), SDLK_s: (0, -1), SDLK_a: (-1, 0), SDLK_d: (1, 0)}


class Idle:
    def enter(self, player):
        player.frame = 0

    def do(self, player):
        pass

    def draw(self, player):
        player.draw_frame(0)


class Run:
    def enter(self, player):
        player.frame = 0

    def do(self, player):
        player.frame = (player.frame + RUN_FPS * game_framework.frame_time) % len(RUN_FRAMES)
        dx, dy = player.dir_x, player.dir_y
        if dx and dy:                         # 대각선은 같은 속도가 되도록 정규화
            dx, dy = dx / math.sqrt(2), dy / math.sqrt(2)
        player.x += dx * MOVE_SPEED * game_framework.frame_time
        player.y += dy * MOVE_SPEED * game_framework.frame_time
        half_w, half_h = DRAW_W // 2, DRAW_H // 2
        player.x = max(half_w, min(get_canvas_width() - half_w, player.x))
        player.y = max(half_h, min(get_canvas_height() - half_h, player.y))

    def draw(self, player):
        player.draw_frame(RUN_FRAMES[int(player.frame)])


class Player:
    def __init__(self):
        self.x, self.y = get_canvas_width() // 2, get_canvas_height() // 2
        self.image = load_image('resource/horong_sheet.png')
        self.frame = 0
        self.dir_x, self.dir_y = 0, 0
        self.pressed_keys = set()

        self.states = {'IDLE': Idle(), 'RUN': Run()}
        self.machine = Machine(
            model=self,
            states=['IDLE', 'RUN'],
            transitions=[
                {'trigger': 'start_run', 'source': 'IDLE', 'dest': 'RUN'},
                {'trigger': 'stop_run', 'source': 'RUN', 'dest': 'IDLE'},
            ],
            initial='IDLE',
            auto_transitions=False,
        )

    def on_enter_IDLE(self):
        self.states['IDLE'].enter(self)

    def on_enter_RUN(self):
        self.states['RUN'].enter(self)

    # ---- 입력 ----
    def handle_event(self, event):

        if event.type not in (SDL_KEYDOWN, SDL_KEYUP) or event.key not in MOVE_KEYS:
            return
        if event.type == SDL_KEYDOWN:
            self.pressed_keys.add(event.key)
        else:
            self.pressed_keys.discard(event.key)

        self.dir_x = sum(MOVE_KEYS[k][0] for k in self.pressed_keys)
        self.dir_y = sum(MOVE_KEYS[k][1] for k in self.pressed_keys)

        moving = self.dir_x != 0 or self.dir_y != 0
        if moving and self.state == 'IDLE':
            self.start_run()
        elif not moving and self.state == 'RUN':
            self.stop_run()

    def pause(self):
        self.pressed_keys.clear()
        self.dir_x, self.dir_y = 0, 0
        if self.state == 'RUN':
            self.stop_run()

    # ---- 매 프레임 ----
    def update(self):
        self.states[self.state].do(self)

    def draw_frame(self, index):
        self.image.clip_draw(index * FRAME_W, 0, FRAME_W, FRAME_H, self.x, self.y, DRAW_W, DRAW_H)

    def draw(self):
        self.states[self.state].draw(self)
