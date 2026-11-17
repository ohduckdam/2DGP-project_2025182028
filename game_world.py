# 레이어 순서대로 그린다. 어둠은 캐릭터 위, UI 아래.
BACKGROUND, OBJECT, DARKNESS, UI = 0, 1, 2, 3

world = [[], [], [], []]


def add_object(o, depth=OBJECT):
    world[depth].append(o)


def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return


def update():
    for layer in world:
        for o in layer[:]:
            o.update()


def render():
    for layer in world:
        for o in layer[:]:
            o.draw()


def clear():
    for layer in world:
        layer.clear()
