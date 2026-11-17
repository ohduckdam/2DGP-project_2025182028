# pico2d 의 get_events() 는 마우스 휠 이벤트를 넘겨주지 않는다.
# 그래서 같은 방식으로 SDL 이벤트를 직접 읽되, 휠 이벤트(SDL_MOUSEWHEEL)도 함께 넘겨주는 함수를 만든다.
# 사용법은 pico2d 의 get_events() 와 같다. 휠 이벤트는 event.wheel 에 +1(위로) / -1(아래로)이 들어있다.
import ctypes

from sdl2 import (SDL_Event, SDL_PollEvent, SDL_QUIT, SDL_KEYDOWN, SDL_KEYUP,
                  SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP, SDL_MOUSEWHEEL)


class Event:
    def __init__(self, event_type):
        self.type = event_type
        self.key = None
        self.button = None
        self.x = None
        self.y = None
        self.wheel = 0


def get_events():
    sdl_event = SDL_Event()
    event_list = []
    while SDL_PollEvent(ctypes.byref(sdl_event)):
        t = sdl_event.type
        if t == SDL_QUIT:
            event_list.append(Event(t))
        elif t in (SDL_KEYDOWN, SDL_KEYUP):
            if sdl_event.key.repeat:        # 키를 꾹 누를 때 생기는 반복 입력은 무시
                continue
            e = Event(t)
            e.key = sdl_event.key.keysym.sym
            event_list.append(e)
        elif t == SDL_MOUSEMOTION:
            e = Event(t)
            e.x, e.y = sdl_event.motion.x, sdl_event.motion.y
            event_list.append(e)
        elif t in (SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP):
            e = Event(t)
            e.button, e.x, e.y = sdl_event.button.button, sdl_event.button.x, sdl_event.button.y
            event_list.append(e)
        elif t == SDL_MOUSEWHEEL:
            if sdl_event.wheel.y != 0:
                e = Event(t)
                e.wheel = 1 if sdl_event.wheel.y > 0 else -1
                event_list.append(e)
    return event_list
