import pygame as pg
import random
from .utilidades import *


class Lobo(pg.sprite.Sprite):
    # Responsável por cada lobo vivo
    lobos_vivos = []

    def __init__(self, velocidade_padrao, nome, instancia_retangulo, vida):
        super().__init__()
        w = pg.display.get_surface().get_width()
        h = pg.display.get_surface().get_height()
        self.largura = w / (25.6)
        self.altura = h / (14.4)
        self.nome = nome
        self.velocidade_padrao = velocidade_padrao
        self.velocidade = self.velocidade_padrao
        self.raio = 100 # caso o raio do lobo for diferente do raio dos outros animais, talvez exista um problema na colisão entre eles
        self.vida = vida
        self.direcao = False
        self.repouso = 0
        self.retangulo = instancia_retangulo
        Lobo.lobos_vivos.append(self)

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
                for lobo in Lobo.lobos_vivos:
                    if lobo != self and ((lobo.x + (lobo.largura / 2) - valorx) ** 2 + (lobo.y + (lobo.altura / 2) - valory)** 2) ** (1/2) < lobo.raio:
                        escolher = False
                bloqueio = []
                for k in paredes:
                    bloqueio.append(k)
                for k in rios:
                    bloqueio.append(k)
                for bloqueador in bloqueio:
                    if colisao_amigavel(self, bloqueador):
                        escolher = False

    def desenhar_lobo(self, janela):
        # Falta adicionar imagens/animações do lobo
        lobo_imagem = pg.transform.smoothscale(pg.image.load('assets/lobo.png'), (50,50))
        
        if self.direcao == 'direita' or self.direcao == False: # O lobo sendo inicialmente desenhado para o lado direito
            janela.blit(lobo_imagem, (self.x, self.y))
        elif self.direcao == 'esquerda':
            janela.blit(lobo_imagem, (self.x, self.y))
        elif self.direcao == 'cima':
            janela.blit(lobo_imagem, (self.x, self.y))
        elif self.direcao == 'baixo':
            janela.blit(lobo_imagem, (self.x, self.y))

    def morte(self):
        Lobo.lobos_vivos.remove(self)
    
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

        if ((distancia_x)**2 + (distancia_y)**2)**(1/2) <= raio_alerta:
            if abs(distancia_x) > abs(distancia_y):
                self.velocidade = self.velocidade_padrao
                if distancia_x < 0:
                    self.direcao = 'esquerda'
                else:
                    self.direcao = 'direita'
            else:
                if distancia_y < 0:
                    self.direcao = 'cima'
                else:
                    self.direcao = 'baixo'
        else:
            self.velocidade = 0

        if self.direcao == 'direita':
            self.x += self.velocidade * variacao_tempo
        elif self.direcao == 'esquerda':
            self.x -= self.velocidade * variacao_tempo
        elif self.direcao == 'baixo':
            self.y += self.velocidade * variacao_tempo
        elif self.direcao == 'cima':
            self.y -= self.velocidade * variacao_tempo
        self.velocidade = self.velocidade_padrao
        bloqueio = []
        for k in Lobo.lobos_vivos:
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
