import pygame as pg
import random
from .utilidades import *
from .dragao import *

class Animais(pg.sprite.Sprite):
    # Responsável por cada animal vivo
    animais_vivos = []

    def __init__(self, infos, nome, instancia_mago):
        super().__init__()
        w = pg.display.get_surface().get_width()
        h = pg.display.get_surface().get_height()
        self.largura = w / (25.6)
        self.altura = h / (14.4)
        self.nome = nome
        self.velocidade_padrao = infos[self.nome]['velocidade']
        self.velocidade = self.velocidade_padrao
        self.esquerda = infos[self.nome]['referencia']['esquerda']
        self.direita = infos[self.nome]['referencia']['direita']
        self.cima = infos[self.nome]['referencia']['cima']
        self.baixo = infos[self.nome]['referencia']['baixo']
        self.img = self.baixo
        self.raio = 100
        self.direcao = False
        self.mov_idle = 0
        self.velocidade_idle = 0.03
        self.repouso = 0
        self.mago = instancia_mago
        Animais.animais_vivos.append(self)

    def spawnar(self, mago, paredes, rios, dragao):
        w = pg.display.get_surface().get_width()
        h = pg.display.get_surface().get_height()
        escolher = False
        while not escolher:	
            valorx = random.randint(0, w)	
            valory = random.randint(0, h - 60)
            # Só irão nascer animais em um raio maior que 300 px
            if ((mago.x + (mago.largura / 2) - valorx) ** 2 + (mago.y + (mago.altura / 2) - valory)** 2) ** (1/2) >= mago.raio:	
                self.x = valorx	
                self.y = valory	
                escolher = True
                for animal in Animais.animais_vivos:
                    if animal != self and ((animal.x + (animal.largura / 2) - valorx) ** 2 + (animal.y + (animal.altura / 2) - valory)** 2) ** (1/2) < animal.raio:
                        escolher = False
                bloqueio = []
                for k in paredes:
                    bloqueio.append(k)
                for k in rios:
                    bloqueio.append(k)
                for k in dragao:
                    bloqueio.append(k)
                for bloqueador in bloqueio:
                    if colisao_amigavel(self, bloqueador):
                        escolher = False

    def desenhar_animal(self, janela):
        janela.blit(self.img, (self.x, self.y))
        
    def morte(self):
        Animais.animais_vivos.remove(self)
    
    def move(self, mago, variacao_tempo, paredes, rios, dragao, velocidade_devagar, velocidade_rapida):
        raio_alerta = mago.raio
        if mago.velocidade == velocidade_rapida:
            raio_alerta = raio_alerta * 1.5
        elif mago.velocidade == velocidade_devagar:
            raio_alerta = raio_alerta / 1.5
        distancia_x = mago.x - self.x
        distancia_y = mago.y - self.y
        antigo_x = self.x
        antigo_y = self.y
        direcoes = ['direita', 'esquerda', 'baixo', 'cima']
        if not self.direcao and self.repouso == 0:
            self.direcao = random.choice(direcoes)
            self.repouso = random.randint(160, 240)
            self.mov_idle = random.randint(120,150)
            self.velocidade = self.velocidade_idle
        if self.mov_idle == 0:
            self.direcao = False
            self.velocidade = self.velocidade_padrao
        else: 
            self.mov_idle -= 1
        if self.repouso > 0:
            self.repouso -= 1

        if ((distancia_x)**2 + (distancia_y)**2)**(1/2) <= raio_alerta:
            self.mov_idle = 0
            if abs(distancia_x) > abs(distancia_y):
                self.velocidade = self.velocidade_padrao
                if distancia_x < 0:
                    self.direcao = 'direita'
                else:
                    self.direcao = 'esquerda'
            else:
                if distancia_y < 0:
                    self.direcao = 'baixo'
                else:
                    self.direcao = 'cima'

        if self.direcao == 'direita':
            self.x += self.velocidade * variacao_tempo
            self.img = self.direita
        elif self.direcao == 'esquerda':
            self.img = self.esquerda
            self.x -= self.velocidade * variacao_tempo
        elif self.direcao == 'baixo':
            self.img = self.baixo
            self.y += self.velocidade * variacao_tempo
        elif self.direcao == 'cima':
            self.img = self.cima
            self.y -= self.velocidade * variacao_tempo
        bloqueio = []
        for k in Animais.animais_vivos:
            if k != self:
                bloqueio.append(k)
        for k in paredes:
            bloqueio.append(k)
        for k in rios:
            bloqueio.append(k)
        for k in dragao:
            bloqueio.append(k)
        for animal in bloqueio:
            if colisao_amigavel(self, animal):
                self.x = antigo_x
                self.y = antigo_y
