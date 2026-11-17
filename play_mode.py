from pico2d import clear_canvas, update_canvas, get_events
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE

import game_framework
import game_world


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()


def init():
    pass


def finish():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def update():
    game_world.update()


def render():
    clear_canvas()
    game_world.render()
    update_canvas()
