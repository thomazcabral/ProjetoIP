import pygame as pg
import random
import os

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
    def __init__(self, proporcao, instancia_retangulo, rios):
        w = pg.display.get_surface().get_width()
        h = pg.display.get_surface().get_height()
        self.largura = ((w + h) / 2) * proporcao
        self.altura = self.largura / 2
        escolher = False
        self.retangulo = instancia_retangulo
        i = 0
        while not escolher and i < 500:
            i += 1
            self.x = random.randrange(0, int(w - self.largura))
            self.y = random.randrange(50, int(h - 60 - self.altura))
            if not colisao_amigavel(self, self.retangulo):
                escolher = True
            for parede in Parede.paredes:
                if ((parede.x + (parede.largura / 2) - self.x) ** 2 + (parede.y + (parede.altura / 2) - self.y)** 2) ** (1/2) < parede.raio:
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
        self.img = pg.image.load('assets/folhas.png')
        self.img.set_alpha(210)
        x = self.img.get_size()[0]
        y = self.img.get_size()[1]
        escala = self.largura * 3/ x
        redimensionar = pg.transform.smoothscale(self.img, ((x*escala), (y*escala)))
        janela.blit(redimensionar, (self.x - (self.largura), self.y - 5 * self.altura))