import pygame as pg
from .vector2d import Vector2d

directions = {
    "RIGHT": Vector2d(1, 0),
    "LEFT": Vector2d(-1, 0),
    "UP": Vector2d(0, -1), 
    "DOWN": Vector2d(0, 1),
}
directions_inv = {
    Vector2d(1, 0): "RIGHT",
    Vector2d(-1, 0): "LEFT",
    Vector2d(0, -1): "UP", 
    Vector2d(0, 1): "DOWN",
    Vector2d(0, 0): "DOWN"
}

directions_img = {
    Vector2d(1, 0): "assets/mago_right.png",
    Vector2d(-1, 0): "assets/mago_left.png",
    Vector2d(0, -1): "assets/mago_up.png", 
    Vector2d(0, 1): "assets/mago_down.png",
    Vector2d(0, 0): "assets/mago_down.png"
}

def get_direction(keys, setas):
    if keys[pg.K_RIGHT] or keys[pg.K_d]:
        setas['RIGHT'] += 1
    else:
        setas['RIGHT'] = 0
    if keys[pg.K_LEFT] or keys[pg.K_a]:
        setas['LEFT'] += 1
    else:
        setas['LEFT'] = 0
    if keys[pg.K_UP] or keys[pg.K_w]:
        setas['UP'] += 1
    else:
        setas['UP'] = 0
    if keys[pg.K_DOWN] or keys[pg.K_s]:
        setas['DOWN'] += 1
    else:
        setas['DOWN'] = 0
    
    chosen = sorted(setas.items(), key=lambda seta: seta[1], reverse=True)

    if chosen[0][1] > 0:
        if chosen[1][1] > 0:
            return directions[chosen[1][0]]
        else:
            return directions[chosen[0][0]]
