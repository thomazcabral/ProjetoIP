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
        self.img = self.baixo[0]
        self.raio = 100
        self.direcao = False
        self.mov_idle = 0
        self.velocidade_idle = 0.03
        self.repouso = 0
        self.mago = instancia_mago
        self.estagio = 0
        self.encurralado = False
        self.x = 0
        self.y = 0
        Animais.animais_vivos.append(self)

    def spawnar(self, mago, paredes, rios, dragao, offset_x, offset_y):
        w = pg.display.get_surface().get_width()
        h = pg.display.get_surface().get_height()
        escolher = False
        while not escolher:	
            valorx = random.randint(int(offset_x), int(offset_x + w))	
            valory = random.randint(int(offset_y), int(offset_y + h - 60))
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

    def desenhar_animal(self, janela, offset_x, offset_y):
        janela.blit(self.img, (self.x - offset_x, self.y - offset_y))
        
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
            self.repouso = random.randrange(150, 180)
            self.mov_idle = random.randrange(120,150, 6)
            self.velocidade = self.velocidade_idle
        if self.estagio == 0 and self.mov_idle == 0:
            self.encurralado = False
            self.direcao = False
            self.velocidade = self.velocidade_padrao
        if self.mov_idle > 0: 
            self.mov_idle -= 1
        if self.repouso > 0:
            self.repouso -= 1

        if not self.encurralado and self.estagio == 0 and  ((distancia_x)**2 + (distancia_y)**2)**(1/2) <= raio_alerta:
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
            self.estagio += 0.25
            self.img = self.direita[int(self.estagio % 3)]
        elif self.direcao == 'esquerda':
            self.estagio += 0.25
            self.img = self.esquerda[int(self.estagio % 3)]
            self.x -= self.velocidade * variacao_tempo
        elif self.direcao == 'baixo':
            self.estagio += 0.25
            self.img = self.baixo[int(self.estagio % 3)]
            self.y += self.velocidade * variacao_tempo
        elif self.direcao == 'cima':
            self.estagio += 0.25
            self.img = self.cima[int(self.estagio % 3)]
            self.y -= self.velocidade * variacao_tempo
        if self.estagio == 3:
            self.estagio = 0
        bloqueio = []
        horizontal = ['esquerda', 'direita']
        vertical = ['cima', 'baixo']
        for k in Animais.animais_vivos:
            if k != self:
                bloqueio.append(k)
        for k in paredes:
            bloqueio.append(k)
        for k in rios:
            bloqueio.append(k)
        for k in dragao:
            bloqueio.append(k)
        for coisa in bloqueio:
            if colisao_amigavel(self, coisa):
                self.encurralado = True
                self.mov_idle = 36
                self.x = antigo_x
                self.y = antigo_y
                if self.direcao in horizontal:
                    self.direcao = random.choice(vertical)
                elif self.direcao in vertical:
                    self.direcao = random.choice(horizontal)

