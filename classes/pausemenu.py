import pygame as pg
import sys
import os
import time
from classes import Menu


class Button:
    def __init__(self, text, x, y):
        self.rect = pg.Rect(0, 0, 200, 50)
        self.rect.center = (x, y)
        self.text = text

class PauseMenu:
    def __init__(self, engine, screen):
        pg.init()
        self.menu = Menu()
        self.engine = engine  
        self.is_visible = False
        self.paused = True
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        font_path = os.path.abspath("assets/Flavors-Regular.ttf")
        self.font = pg.font.Font(font_path, 36)

        
        button_y = screen.get_height() // 2 - 50
        button_spacing = 60  
        self.resume_button = Button("Resume", screen.get_width() // 2, button_y)
        self.restart_button = Button("Restart", screen.get_width() // 2, button_y + button_spacing)
        self.quit_button = Button("Quit", screen.get_width() // 2, button_y + 2 * button_spacing)
        self.buttons = [self.resume_button, self.restart_button, self.quit_button]

        self.is_visible = False

    def draw(self):
        if self.is_visible:
            self.img = pg.image.load('assets/pause.png')
            self.resized_image = pg.transform.scale(self.img, (self.screen.get_width() // 1, self.screen.get_height() // 1))
            self.image_width, self.image_height = self.resized_image.get_size()
            self.x = (self.screen.get_width() - self.image_width) // 2
            self.y = (self.screen.get_height() - self.image_height) // 2
            self.screen.blit(self.resized_image, (self.x, self.y))

            for button in self.buttons:
                pg.draw.rect(self.screen, (	24, 97, 90), button.rect, border_radius=10)
                
                text = self.font.render(button.text, True, (52, 14, 56)) 
                text_rect = text.get_rect(center=button.rect.center)
                self.screen.blit(text, text_rect)

    def handle_event(self, event, old_time):
        if event.type == pg.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    action = button.text
                    self.handle_action(action, old_time) 

    def handle_action(self, action, old_time):
        if action == "Resume":
            self.engine.paused = False
            self.engine.tempo_restante = old_time
            self.engine.duracao_timer = old_time
            self.engine.comeco_timer = time.time()  
            self.toggle()

        elif action == "Restart":
            self.engine.running = False
            self.engine.should_restart = True
            self.engine.paused = False

        elif action == "Quit":
            sys.exit()  

    def toggle(self):
        self.is_visible = not self.is_visible