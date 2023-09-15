import pygame as pg
import sys
from objects import *

pg.init()

# Set up screen dimensions
screen_width = 1200
screen_height = 650
screen = pg.display.set_mode((screen_width, screen_height))

# Define colors
white = (255, 255, 255)

# Initial player position
position = Vector2d(200, 200)
initial_direction = Vector2d(0, 0)
dimension = Vector2d(75, 75)
speed = 2
stamina = 1000

speed_factor = 5

player = Player(position, initial_direction, dimension, speed, stamina)

clock = pg.time.Clock()
setas = {'RIGHT': 0, 'LEFT': 0, 'UP': 0, 'DOWN': 0}

running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    keys = pg.key.get_pressed()
    # Se alguma tecla estiver sendo pressionada, vai ser o ´direction´
    
    direction = get_direction(keys, setas)
    if direction:
        player.direction = direction
        if keys[pg.K_SPACE]:
            if stamina > 0:
                player.speed = speed_factor
                stamina -= 2
        else:
            stamina += 1
        player.move()
    player.speed = speed
    screen.fill(white)
    player.draw(screen)
    pg.display.update()

    # Limit the frame rate
    clock.tick(60)

# Quit Pygame
pg.quit()
sys.exit()

