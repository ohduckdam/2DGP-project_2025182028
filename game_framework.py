import time

running = False
stack = []
frame_time = 0.0   # 직전 프레임에 걸린 시간(초). 이동 속도 등에 곱해서 사용


def change_mode(mode):
    if stack:
        stack.pop().finish()
    stack.append(mode)
    mode.init()


def push_mode(mode):
    if stack:
        stack[-1].pause()
    stack.append(mode)
    mode.init()


def pop_mode():
    if stack:
        stack.pop().finish()
    if stack:
        stack[-1].resume()
    else:
        quit()


def quit():
    global running
    running = False


def run(start_mode):
    global running, stack, frame_time
    running = True
    stack = [start_mode]
    try:
        start_mode.init()
        current_time = time.time()
        while running:
            stack[-1].handle_events()
            stack[-1].update()
            stack[-1].render()
            time.sleep(0.01)
            now = time.time()
            frame_time = min(now - current_time, 0.1)   # 창을 끌 때 등 큰 값이 튀지 않도록 제한
            current_time = now
    finally:
        while stack:
            stack.pop().finish()
        running = False
