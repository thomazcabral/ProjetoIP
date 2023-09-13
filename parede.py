import pygame as pg
import random


PRETO = (0, 0, 0)
LARGURA = 1280
ALTURA = 720
janela = pg.display.set_mode((LARGURA, ALTURA))



def colisao_amigavel(objeto1, objeto2):
    if (objeto2.x + objeto2.largura >= objeto1.x >= objeto2.x or objeto1.x + objeto1.largura >= objeto2.x >= objeto1.x) and (objeto2.y + objeto2.altura >= objeto1.y >= objeto2.y or objeto1.y + objeto1.altura >= objeto2.y >= objeto1.y):
        return True


class Parede:
    paredes = []
    raio = 200
    def __init__(self, proporcao, instancia_retangulo):
        w = pg.display.get_surface().get_width()
        h = pg.display.get_surface().get_height()
        self.largura = self.altura = ((w + h) / 2) * proporcao
        self.raio = Parede.raio 
        escolher = False
        self.retangulo = instancia_retangulo
        while not escolher:
            self.x = random.randrange(0, int(w - self.largura))
            self.y = random.randrange(50, int(h - 60 - self.altura))
            if not colisao_amigavel(self, self.retangulo):
                escolher = True
            for parede in Parede.paredes:
                if ((parede.x + (parede.largura / 2) - self.x) ** 2 + (parede.y + (parede.altura / 2) - self.y)** 2) ** (1/2) < parede.raio:
                    escolher = False

        Parede.paredes.append(self)
    def desenhar_parede(self):
        pg.draw.rect(janela, PRETO, (self.x, self.y, self.largura, self.altura))
