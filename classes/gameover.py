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

class GameoverMenu:
    def __init__(self, engine, screen):
        pg.init()
        self.menu = Menu()
        self.engine = engine  
        self.is_visible = True
        self.paused = True
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        font_path = os.path.abspath("assets/Flavors-Regular.ttf")
        self.font = pg.font.Font(font_path, 36)
        
       

        self.is_visible = False

        self.img = pg.image.load('assets/gameover1.png')
        self.resized_image = pg.transform.scale(self.img, (screen.get_width() // 1, screen.get_height() // 1))
        self.image_width, self.image_height = self.resized_image.get_size()
        self.x = (screen.get_width() - self.image_width) // 2
        self.y = (screen.get_height() - self.image_height) // 2

        pixels = pg.surfarray.array3d(self.screen)

         # Convert the RGB values to grayscale
        grayscale_pixels = 0.2989 * pixels[..., 0] + 0.5870 * pixels[..., 1] + 0.1140 * pixels[..., 2]

        # Convert the grayscale pixel values back to RGB format
        grayscale_image = pg.surfarray.make_surface(grayscale_pixels)
        self.grayscale_image = pg.transform.scale(grayscale_image, (self.screen.get_width(), self.screen.get_height()))


    def draw(self):
        button_y = self.screen.get_height() // 2 - 50
        button_spacing = 60

        self.buttons_value_list = []

        for animal in reversed(self.engine.pontos_animais.keys()): #contador dos animais
            if self.engine.pontos_animais[animal] < 10:
                contador = f'{self.engine.pontos_animais[animal]}'
            else:
                contador = f'{self.engine.pontos_animais[animal]}'
            self.buttons_value_list.append(contador)

        self.animal1 = Button(self.buttons_value_list[2], self.screen.get_width() // 2, button_y)
        self.animal2 = Button(self.buttons_value_list[1], self.screen.get_width() // 2, button_y + button_spacing)
        self.animal3 = Button(self.buttons_value_list[0], self.screen.get_width() // 2, button_y + 2 * button_spacing)
        self.dragao = Button(f'{self.engine.dragon_kills}', self.screen.get_width() // 2, button_y + 3 * button_spacing)

        self.buttons = [self.animal1, self.animal2, self.animal3, self.dragao]

       

        for y in range(self.screen.get_height()):
            for x in range(self.screen.get_width()):
                pixel_color = self.screen.get_at((x, y))  # Get the color of the current pixel
                grayscale_value = (pixel_color.r + pixel_color.g + pixel_color.b) // 3
                grayscale_color = (grayscale_value, grayscale_value, grayscale_value)
                self.screen.set_at((x, y), grayscale_color)  # Set the pixel to the grayscale color

        self.screen.blit(self.resized_image, (self.x, self.y))
        for button in self.buttons:
            pg.draw.rect(self.screen, (	24, 97, 90), button.rect, border_radius=10)
            text = self.font.render(button.text, True, (52, 14, 56)) 
            text_rect = text.get_rect(center=button.rect.center)
            self.screen.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.engine.running = False
                self.engine.should_restart = True
                return True