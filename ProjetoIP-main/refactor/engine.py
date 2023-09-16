import pygame as pg
import sys
from objects import Player, get_direction

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
        player = Player(*self.player_config)
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
                  
                    player.speed = 3
            
    
                player.move()
            player.speed = 1
            screen.fill(self.colors['WHITE'])
            player.draw(screen)
            pg.display.update()

            # Limit the frame rate
            clock.tick(60)

        # Quit Pygame
        pg.quit()
        sys.exit()
    
    def check_colison(self):
        raise NotImplementedError

    


