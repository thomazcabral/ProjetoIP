import pygame as pg
import random
from .utilidades import *

class Inimigos(pg.sprite.Sprite):
    # Responsável por cada animal vivo
    inimigos_vivos = []

    def __init__(self, infos, nome, instancia_retangulo):
        super().__init__()
        w = pg.display.get_surface().get_width()
        h = pg.display.get_surface().get_height()
        self.largura = w / (25.6)
        self.altura = h / (14.4)
        self.nome = nome
        self.velocidade_padrao = infos[self.nome]['velocidade']
        self.velocidade = self.velocidade_padrao
        self.cor = infos[self.nome]['referencia']
        self.raio = 100
        self.direcao = False
        self.mov_idle = 0
        self.velocidade_idle = 0.03
        self.repouso = 0
        self.retangulo = instancia_retangulo
        Inimigos.inimigos_vivos.append(self)

    def spawnar(self, retangulo, paredes, rios):
        w = pg.display.get_surface().get_width()	
        h = pg.display.get_surface().get_height()	
        escolher = False
        while not escolher:	
            valorx = random.randint(0, w)	
            valory = random.randint(0, h - 60)
            # Só irão nascer animais em um raio maior que 300 px
            if ((retangulo.x + (retangulo.largura / 2) - valorx) ** 2 + (retangulo.y + (retangulo.altura / 2) - valory)** 2) ** (1/2) >= retangulo.raio:	
                self.x = valorx	
                self.y = valory	
                escolher = True
                for inimigo in Inimigos.inimigos_vivos:
                    if inimigo != self and ((inimigo.x + (inimigo.largura / 2) - valorx) ** 2 + (inimigo.y + (inimigo.altura / 2) - valory)** 2) ** (1/2) < inimigo.raio:
                        escolher = False
                bloqueio = []
                for k in paredes:
                    bloqueio.append(k)
                for k in rios:
                    bloqueio.append(k)
                for bloqueador in bloqueio:
                    if colisao_amigavel(self, bloqueador):
                        escolher = False

    def desenhar_inimigo(self, janela):
        janela.blit(self.cor, (self.x, self.y))
        
    def morte(self):
        Inimigos.inimigos_vivos.remove(self)
    
    def move(self, retangulo, variacao_tempo, paredes, rios, velocidade_devagar, velocidade_rapida):
        raio_alerta = retangulo.raio
        if retangulo.velocidade == velocidade_rapida:
            raio_alerta = raio_alerta * 1.5
        elif retangulo.velocidade == velocidade_devagar:
            raio_alerta = raio_alerta / 1.5
        distancia_x = retangulo.x - self.x
        distancia_y = retangulo.y - self.y
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
        elif self.direcao == 'esquerda':
            self.x -= self.velocidade * variacao_tempo
        elif self.direcao == 'baixo':
            self.y += self.velocidade * variacao_tempo
        elif self.direcao == 'cima':
            self.y -= self.velocidade * variacao_tempo
        bloqueio = []
        for k in Inimigos.inimigos_vivos:
            if k != self:
                bloqueio.append(k)
        for k in paredes:
            bloqueio.append(k)
        for k in rios:
            bloqueio.append(k)
        for inimigo in bloqueio:
            if colisao_amigavel(self, inimigo):
                self.x = antigo_x
                self.y = antigo_y
