import pygame as pg
import random
from .functions import *

largura_camera = 1280
altura_camera = 720
janela = pg.display.set_mode((largura_camera, altura_camera))

class Parede:
    paredes = []
    raio = 200
    def __init__(self, proporcao, instancia_mago, rios, LARGURA_MAPA, ALTURA_MAPA):
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
        bloqueio = [instancia_mago]
        for parede in Parede.paredes:
           bloqueio.append(parede)
        while not escolher and i < 500:
            i += 1
            self.x = random.randint(0, int(LARGURA_MAPA - self.largura))
            self.y = random.randint(50, int(ALTURA_MAPA - 60 - self.altura))
            if not colisao_amigavel(self, instancia_mago):
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
        
    def desenhar_tronco(self, offset_x, offset_y):
        self.img = pg.image.load('assets/tronco.png')
        x = self.img.get_size()[0]
        y = self.img.get_size()[1]
        escala = self.largura * 2/ x
        redimensionar = pg.transform.smoothscale(self.img, ((x*escala), (y*escala)))
        janela.blit(redimensionar, (self.x - (self.largura / 2) - offset_x, self.y - offset_y))

    def desenhar_folhas(self, offset_x, offset_y):
        if self.frutifera:
            self.img = pg.image.load('assets/folhas_frutiferas.png')
        else:
            self.img = pg.image.load('assets/folhas.png')
        self.img.set_alpha(210)
        x = self.img.get_size()[0]
        y = self.img.get_size()[1]
        escala = self.largura * 3/ x
        redimensionar = pg.transform.smoothscale(self.img, ((x*escala), (y*escala)))
        janela.blit(redimensionar, (self.x - (self.largura) - offset_x, self.y - 5 * self.altura - offset_y))
