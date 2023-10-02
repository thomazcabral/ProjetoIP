import pygame as pg
import sys

class Menu:
    def __init__(self):
        self.start_game = False

    def show_menu(self, screen):
       
        font = pg.font.Font("assets/Flavors-Regular.ttf", 36)
        button_text_color = (71, 19, 0)

        # Formatação do botão
        button_color = (39, 159, 39) 
        button_color2 = (99, 25, 34) 
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


        end_button = pg.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 + 25, 200, 50)
        end_text = font.render("Quit", True, button_text_color)
        end_text_rect = end_text.get_rect()
        end_text_rect.center = end_button.center

        buttons = [(start_button, "Start"), (end_button, "Quit")]

        while not self.start_game:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button[0].collidepoint(event.pos):
                            action = button[1]
                            if action == "Start":
                                button_color = (14, 57, 14)
                                pg.draw.rect(screen, button_color, start_button)
                                pg.draw.rect(screen, button_color, start_button, border_radius=10)
                                pg.display.flip()
                                self.start_game = True
                            elif action == "Quit":
                                button_color2 = (99, 25, 34) 
                                pg.draw.rect(screen, button_color2, end_button)
                                pg.draw.rect(screen, button_color2, end_button, border_radius=10)
                                pg.display.flip()
                                sys.exit()
                      
            screen.fill((0, 0, 0))

            # Desenhar background e título
            screen.blit(background_image, background_rect)
            screen.blit(title_image, title_rect)

            # Desenhar botão
            pg.draw.rect(screen, button_color, start_button, border_radius=10)
            pg.draw.rect(screen, button_border_color, start_button, button_border_width, border_radius=10)
            pg.draw.rect(screen, button_color2, end_button, border_radius=10)
            pg.draw.rect(screen, button_border_color, end_button, button_border_width, border_radius=10)
            screen.blit(start_text, start_text_rect)
            screen.blit(end_text, end_text_rect)

            pg.display.flip()