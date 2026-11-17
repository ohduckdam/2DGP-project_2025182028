from pico2d import load_image, get_canvas_width, get_canvas_height


class Background:
    def __init__(self):
        self.image = load_image('resource/background.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(get_canvas_width() // 2, get_canvas_height() // 2)
