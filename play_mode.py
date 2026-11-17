from pico2d import clear_canvas, update_canvas, get_events
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE

import game_framework
import game_world
from background import Background
from player import Player
from ui import OilGauge

player = None


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_event(event)


def init():
    global player
    player = Player()

    game_world.add_object(Background(), game_world.BACKGROUND)
    game_world.add_object(player, game_world.OBJECT)
    game_world.add_object(OilGauge(player), game_world.UI)


def finish():
    global player
    game_world.clear()
    player = None


def pause():
    player.pause()


def resume():
    pass


def update():
    game_world.update()


def render():
    clear_canvas()
    game_world.render()
    update_canvas()
