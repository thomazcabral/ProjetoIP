import pygame as pg
import random
from .utilidades import *
from .retangulo import retangulo


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
            if not colisao_amigavel(self, retangulo):
                escolher = True
            for parede in Parede.paredes:
                if ((parede.x + (parede.largura / 2) - self.x) ** 2 + (parede.y + (parede.altura / 2) - self.y)** 2) ** (1/2) < parede.raio:
                    escolher = False

        Parede.paredes.append(self)
    def desenhar_parede(self):
        pg.draw.rect(janela, PRETO, (self.x, self.y, self.largura, self.altura))
