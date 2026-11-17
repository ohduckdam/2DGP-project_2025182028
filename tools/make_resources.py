# 1주차 리소스 생성 스크립트 (Pillow 필요: pip install pillow)
# 실행: 저장소 최상위 폴더에서  python tools/make_resources.py
# 어둠 마스크 크기나 부드러움을 바꾸고 싶을 때 다시 실행하면 resource/ 폴더 이미지가 새로 만들어진다.
import math
import os
import random

from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'resource')
os.makedirs(OUT, exist_ok=True)

DARK = (5, 4, 15)          # 어둠 색
WARM = (255, 190, 90)      # 등불 빛 색

# 빛 설정 (light.py 의 값과 반드시 같아야 한다)
SPREAD_SIZE = 512          # 확산 마스크 이미지 크기
SPREAD_BASE_R = 128        # 확산 마스크의 기준 빛 반경 (이 반경을 기준으로 확대/축소)


def mix(dark, warm):
    """어둠(투명도 dark)과 등불 빛(투명도 warm)을 끊김 없이 섞은 RGBA 한 픽셀"""
    a = dark + warm * (1 - dark)
    if a <= 0:
        return (0, 0, 0, 0)
    w2 = warm * (1 - dark)
    rgb = tuple(int((d * dark + c * w2) / a) for d, c in zip(DARK, WARM))
    return rgb + (int(255 * a),)


def smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def make_spread_hole():
    """가운데가 뚫린 어둠. 반경 SPREAD_BASE_R 근처에서 부드럽게 어두워진다."""
    n = SPREAD_SIZE
    c = n / 2
    im = Image.new('RGBA', (n, n))
    px = im.load()
    r_in, r_out = SPREAD_BASE_R * 0.55, SPREAD_BASE_R * 1.15
    for y in range(n):
        for x in range(n):
            d = math.hypot(x + 0.5 - c, y + 0.5 - c)
            dark = smooth((d - r_in) / (r_out - r_in))
            warm = 0.12 * max(0.0, 1 - d / r_out)
            px[x, y] = mix(dark, warm)
    im.save(os.path.join(OUT, 'spread_hole.png'))


def make_dark():
    Image.new('RGBA', (4, 4), DARK + (255,)).save(os.path.join(OUT, 'dark.png'))


def make_oil_bar():
    back = Image.new('RGBA', (204, 20), (240, 220, 160, 255))
    ImageDraw.Draw(back).rectangle((2, 2, 201, 17), fill=(20, 16, 36, 255))
    back.save(os.path.join(OUT, 'oil_bar_back.png'))
    Image.new('RGBA', (200, 16), (255, 170, 60, 255)).save(os.path.join(OUT, 'oil_bar_fill.png'))


def make_background():
    """1280x720 숲 바닥. 640x360으로 그린 뒤 2배로 키워 도트 느낌을 낸다."""
    random.seed(7)
    w, h = 640, 360
    im = Image.new('RGB', (w, h), (46, 74, 52))
    d = ImageDraw.Draw(im)
    for _ in range(3600):
        x, y = random.randrange(w), random.randrange(h)
        d.point((x, y), fill=random.choice([(60, 96, 64), (38, 62, 44), (72, 110, 70)]))
    for _ in range(90):
        x, y = random.randrange(w), random.randrange(h)
        d.rectangle((x, y, x + 1, y + 1), fill=random.choice([(230, 200, 90), (200, 120, 160), (180, 200, 240)]))
    for x in range(0, w, 2):
        y = int(190 + 26 * math.sin(x / 60))
        d.rectangle((x, y - 10, x + 2, y + 10), fill=(92, 80, 58))
    trees = [(40, 40), (130, 25), (560, 50), (600, 260), (30, 300), (470, 330), (250, 340), (340, 20), (610, 140), (20, 170)]
    for tx, ty in trees:
        d.rectangle((tx - 3, ty, tx + 3, ty + 16), fill=(70, 46, 30))
        d.ellipse((tx - 18, ty - 24, tx + 18, ty + 8), fill=(24, 54, 34), outline=(14, 30, 20))
        d.ellipse((tx - 12, ty - 20, tx + 4, ty - 6), fill=(36, 74, 46))
    im.resize((w * 2, h * 2), Image.NEAREST).save(os.path.join(OUT, 'background.png'))


if __name__ == '__main__':
    make_spread_hole()
    make_dark()
    make_oil_bar()
    make_background()
    print('resource/ 폴더에 이미지를 만들었습니다.')
