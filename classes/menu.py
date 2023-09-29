import pygame as pg
import sys

class Menu:
    def __init__(self):
        self.start_game = False

    def show_menu(self, screen):
       
        font = pg.font.Font("assets/Flavors-Regular.ttf", 36)
        button_text_color = (71, 19, 76)

        # Formatação do botão
        button_color = (39, 159, 39) 
        button_border_color = (39, 159, 39) 
        button_border_width = 0

        # Imagem de fundo
        background_image = pg.image.load("assets/background.jpg")
        background_image = pg.transform.scale(background_image, (screen.get_width(), screen.get_height()))
        background_rect = background_image.get_rect()

        # Título do jogo
        title_image = pg.image.load("assets/title.png")
        title_rect = title_image.get_rect()
        title_rect.center = (screen.get_width() // 2, 100)

        # Botão start
        start_button = pg.Rect(screen.get_width() // 2 - 100, 300, 200, 50)
        start_text = font.render("Start", True, button_text_color)
        start_text_rect = start_text.get_rect()
        start_text_rect.center = start_button.center

        while not self.start_game:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        # Mudar aparência do botão ao clicar
                        button_color = (14, 57, 14)
                        pg.draw.rect(screen, button_color, start_button)
                        pg.draw.rect(screen, button_color, start_button, border_radius=10)
                        pg.display.flip()
                        self.start_game = True

            screen.fill((0, 0, 0))

            # Desenhar background e título
            screen.blit(background_image, background_rect)
            screen.blit(title_image, title_rect)

            # Desenhar botão
            pg.draw.rect(screen, button_color, start_button, border_radius=10)
            pg.draw.rect(screen, button_border_color, start_button, button_border_width, border_radius=10)
            screen.blit(start_text, start_text_rect)

            pg.display.flip()