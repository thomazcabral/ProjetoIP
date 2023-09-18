import pygame as pg
import math
import sys
import random
import os
from objects import *

class Engine:
    def __init__(self, config):
        self.screen_config = [
            config["screen_config"]["screen_width"],
            config["screen_config"]["screen_height"]
        ]
        self.player_config = [
            config["player_config"]["position"],
            config["player_config"]["initial_direction"],
            config["player_config"]["dimension"],
            config["player_config"]["speed"],
            config["player_config"]["stamina"],
        ]
        self.animal_config = [
            config["animal_config"]["spawn_rate"],
            config["animal_config"]["speed"],
        ]
        self.colors = config["colors_config"]
        
    def run(self):
        pg.init()
        screen = pg.display.set_mode([*self.screen_config])
        player = Player(*self.player_config, image='./assets/mago_down.png')
        clock = pg.time.Clock()
        

        setas = {'RIGHT': 0, 'LEFT': 0, 'UP': 0, 'DOWN': 0}

        running = True
        river = self.river_path(None, 50)
        tiles = self.generate_tiles(50, river)

        

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
                    player.speed = 10
                player.move()
            player.speed = 5
            #screen.fill(self.colors['WHITE'])
            self.draw_tiles(screen, tiles)
            self.draw_entity(screen, player)
            pg.display.update()

            # Limit the frame rate
            clock.tick(30)

        # Quit Pygame
        pg.quit()
        sys.exit()
    
    def generate_tiles(self, k: int, river) -> Group:
        """
        Extrai um grid ixj de um screen mxn, em que cada M[i,j] é 
        um quadrado de dimensões kxk
        Exemplo: screensize = 1200 x 800; k = 10
        grid extraído = 120 x 80 (quadrados 10 x 10)

        Caso não seja exato, e.g. 1203 x 808, o output será 121 x 81 (10 x 10).
        """
        tiles_group = Group()
        m = math.ceil(self.screen_config[0] / k)
        n = math.ceil(self.screen_config[1] / k)
        for i in range(m):
            for j in range(n):
                image = pg.image.load('assets/tile14.png') if (i, j) in river else self.random_tile_image()
                position = Vector2d(k*i, k*j)
                dimension = Vector2d(k, k)
                tile = Tile(position=position, dimension=dimension, image=image, direction=None, speed=None)
                tiles_group.add(tile)
        return tiles_group

    def river_path(self, matrix, k):
        m = math.ceil(self.screen_config[0] / k)
        n = math.ceil(self.screen_config[1] / k)
        matrix = [[0 for i in range(m)] for j in range(n)]
        def is_valid_move(x, y):
            return 0 <= x < m and 0 <= y < n and matrix[x][y] == 0

        m = len(matrix)
        n = len(matrix[0])

        # Start from the top row
        x, y = 0, random.randint(0, n - 1)

        # Define possible moves (left, right, down)
        moves = [(0, -1), (0, 1), (1, 0)]

        path = []

        while True:
            matrix[x][y] = 1  # Mark the cell as part of the river
            path.append((x, y))

            # Randomly shuffle the possible moves
            random.shuffle(moves)

            # Try each possible move
            for dx, dy in moves:
                new_x, new_y = x + dx, y + dy

                if is_valid_move(new_x, new_y):
                    # Make the move
                    x, y = new_x, new_y
                    break
            else:
                # If no valid move is found, we've reached the end of the river
                break

        return path

    def random_tile_image(self) -> str:
        directory_path = './assets/tiles'
        return pg.image.load(random.choice([f'{directory_path}/{tile}' for tile in os.listdir(directory_path)])) if random.randint(1,10) == 1 else pg.image.load(f'assets/tiles/tile1.png')

    def draw_tiles(self, screen: pg.Surface, tiles_group: Group) -> None:
        for tile in tiles_group:
            resized_img = pg.transform.smoothscale(tile.image, tile.dimension.val)
            screen.blit(resized_img, (tile.position.val)) 
    
    def colision(self):
        raise NotImplementedError

    def draw_entity(self, screen: pg.Surface, entity: Entity):
        image = pg.image.load(entity.image)
        resized_img = pg.transform.smoothscale(image, entity.dimension.val)
        screen.blit(resized_img, (entity.position.val))
    
    



