import math
import random
import pygame

def draw_hint(surf, fonts, msgs, t, y=60, show=7.0):
    if t > show:
        return
    font_obj = fonts.small if hasattr(fonts, "small") else fonts
    if isinstance(msgs, str):
        msgs = [msgs]
    for i, msg in enumerate(msgs):
        img = font_obj.render(msg, False, (230, 220, 255))
        r = img.get_rect(midtop=(surf.get_width() // 2, y + i * 12))
        surf.blit(img, r)

class Particles:
    def __init__(self):
        self.items = []

    def add(self, x, y, vx, vy, color, life, size=2):
        self.items.append([x, y, vx, vy, life, life, color, size])

    def burst(self, x, y, color, count=12, speed=55, life_range=(0.3, 0.7)):
        for _ in range(count):
            a = random.uniform(0, 6.283)
            s = random.uniform(0.3, 1.0) * speed
            life = random.uniform(life_range[0], life_range[1])
            self.items.append([x, y, s * math.cos(a), s * math.sin(a), life, life, color, 2])

    def update(self, dt):
        alive = []
        for p in self.items:
            p[4] -= dt
            if p[4] > 0:
                p[0] += p[2] * dt
                p[1] += p[3] * dt
                alive.append(p)
        self.items = alive

    def draw(self, surf, cx=0, cy=0):
        for p in self.items:
            x, y, _, _, _, _, color, size = p
            sx, sy = int(x - cx), int(y - cy)
            if 0 <= sx < surf.get_width() and 0 <= sy < surf.get_height():
                surf.fill(color, (sx, sy, size, size))

class Starfield:
    def __init__(self, width, height, count=60):
        self.width = width
        self.height = height
        self.stars = []
        for _ in range(count):
            self.stars.append([
                random.randrange(width),
                random.randrange(height),
                random.uniform(20, 80),
                random.choice([1, 1, 2])
            ])

    def update(self, dt, speed_mult=1.0):
        for s in self.stars:
            s[1] += s[2] * speed_mult * dt
            if s[1] > self.height:
                s[1] = 0
                s[0] = random.randrange(self.width)

    def draw(self, surf):
        for x, y, _, size in self.stars:
            col = (200, 220, 255) if size == 2 else (130, 140, 180)
            surf.fill(col, (int(x), int(y), size, size))
