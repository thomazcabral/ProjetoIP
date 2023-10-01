import pygame as pg
import random
from .functions import *

# mesma lógica dos animais, mas sem movimentação
class Coletaveis:
    coletaveis_ativos = []

    def __init__(self, nome):
        self.nome = nome
        w = pg.display.get_surface().get_width()
        h = pg.display.get_surface().get_height()
        self.largura = w / (40)
        self.altura = h  / (22.5)
        self.img = pg.transform.scale(pg.image.load(f'assets/{self.nome}.png'), (self.largura, self.altura))
        self.raio = 100
        Coletaveis.coletaveis_ativos.append(self)

    def spawnar(self, mago, paredes, rios, dragao, animais, offset_x, offset_y):
        w = pg.display.get_surface().get_width()
        h = pg.display.get_surface().get_height()
        escolher = False
        while not escolher:	
            valorx = random.randint(int(offset_x), int(offset_x + w))	
            valory = random.randint(int(offset_y), int(offset_y + h - 60))
            if ((mago.x + (mago.largura / 2) - valorx) ** 2 + (mago.y + (mago.altura / 2) - valory)** 2) ** (1/2) >= mago.raio:	
                self.x = valorx	
                self.y = valory	
                escolher = True
                for coletavel in Coletaveis.coletaveis_ativos:
                    if coletavel != self and ((coletavel.x + (coletavel.largura / 2) - valorx) ** 2 + (coletavel.y + (coletavel.altura / 2) - valory)** 2) ** (1/2) < coletavel.raio:
                        escolher = False
                bloqueio = []
                for k in paredes:
                    bloqueio.append(k)
                for k in rios:
                    bloqueio.append(k)
                for k in dragao:
                    bloqueio.append(k)
                for k in animais:
                    bloqueio.append(k)
                for bloqueador in bloqueio:
                    if colisao_amigavel(self, bloqueador):
                        escolher = False
    
    def desenhar_coletavel(self, janela, offset_x, offset_y):
        janela.blit(self.img, (self.x - offset_x, self.y - offset_y))
    
    def morte(self):
        Coletaveis.coletaveis_ativos.remove(self)
            