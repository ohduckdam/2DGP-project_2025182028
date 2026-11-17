from pico2d import open_canvas, close_canvas

import game_framework
import play_mode as start_mode

CANVAS_WIDTH, CANVAS_HEIGHT = 1280, 720

open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
game_framework.run(start_mode)
close_canvas()
