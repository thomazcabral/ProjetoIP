import pygame 
from vector import Vector2d
from objects import Entity
pygame.init()

# Set up screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Define colors
white = (255, 255, 255)

# Initial player position
position = Vector2d(200, 200)
initial_speed = Vector2d(0, 0)
dimension = Vector2d(10, 10)

speed_factor = 10

directions = {
    "RIGHT": Vector2d(1, 0) * speed_factor,
    "LEFT": Vector2d(-1, 0) * speed_factor,
    "UP": Vector2d(0, -1) * speed_factor,
    "DOWN": Vector2d(0, 1) * speed_factor,
}

player = Entity(position, initial_speed, dimension)

clock = pygame.time.Clock()

running = True
setas = {'RIGHT': 0, 'LEFT': 0, 'UP': 0, 'DOWN': 0}
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
        
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        setas['RIGHT'] += 1
    else:
        setas['RIGHT'] = 0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        setas['LEFT'] += 1
    else:
        setas['LEFT'] = 0
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        setas['UP'] += 1
    else:
        setas['UP'] = 0
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        setas['DOWN'] += 1
    else:
        setas['DOWN'] = 0
    
    escolhida = sorted(setas.items(), key=lambda seta: seta[1], reverse=True)
    
    if escolhida[0][1] > 0:
        if escolhida[1][1] > 0:
            player.speed = directions[escolhida[1][0]]
        else:
            player.speed = directions[escolhida[0][0]]
        player.move()
    
    # Clear the screen
    screen.fill(white)

    # Draw the player (a simple rectangle)
    pygame.draw.rect(screen, (0, 0, 255), (*player.position.val, 50, 50))

    # Update the screen
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()

