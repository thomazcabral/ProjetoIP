import pygame as pg
import random
from .utilidades import *

class Parede:
    paredes = []
    raio = 200
    def __init__(self, proporcao, instancia_retangulo, rios):
        w = pg.display.get_surface().get_width()
        h = pg.display.get_surface().get_height()
        frutifera = random.randint(0,1)
        if frutifera == 1:
            self.frutifera = True
        else:
            self.frutifera = False
        self.largura = ((w + h) / 2) * proporcao
        self.altura = self.largura / 2
        escolher = False
        i = 0
        bloqueio = [instancia_retangulo]
        for parede in Parede.paredes:
           bloqueio.append(parede)
        while not escolher and i < 500:
            i += 1
            self.x = random.randint(0, int(w - self.largura))
            self.y = random.randint(50, int(h - 60 - self.altura))
            if not colisao_amigavel(self, instancia_retangulo):
                escolher = True
            for bloqueador in bloqueio:
                if ((bloqueador.x + (bloqueador.largura / 2) - self.x) ** 2 + (bloqueador.y + (bloqueador.altura / 2) - self.y)** 2) ** (1/2) < bloqueador.raio:
                    escolher = False
            for rio in rios:
                if colisao_amigavel(self, rio):
                    escolher = False
        if i == 500:
            self.x = w
            self.y = h
        Parede.paredes.append(self)
        
    def desenhar_tronco(self):
        self.img = pg.image.load('assets/tronco.png')
        x = self.img.get_size()[0]
        y = self.img.get_size()[1]
        escala = self.largura * 2/ x
        redimensionar = pg.transform.smoothscale(self.img, ((x*escala), (y*escala)))
        janela.blit(redimensionar, (self.x - (self.largura / 2), self.y))

    def desenhar_folhas(self):
        if self.frutifera:
            self.img = pg.image.load('assets/folhas_frutiferas.png')
        else:
            self.img = pg.image.load('assets/folhas.png')
        self.img.set_alpha(210)
        x = self.img.get_size()[0]
        y = self.img.get_size()[1]
        escala = self.largura * 3/ x
        redimensionar = pg.transform.smoothscale(self.img, ((x*escala), (y*escala)))
        janela.blit(redimensionar, (self.x - (self.largura), self.y - 5 * self.altura))