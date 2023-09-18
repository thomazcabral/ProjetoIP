import pygame as pg
import random
from .utilidades import *


class Dragao(pg.sprite.Sprite):
    # Responsável por cada dragão vivo
    dragoes_vivos = []

    def __init__(self, velocidade_padrao, nome, instancia_mago, vida):
        super().__init__()
        w = pg.display.get_surface().get_width()
        h = pg.display.get_surface().get_height()
        self.largura = w / (25.6)
        self.altura = h / (14.4)
        self.nome = nome
        self.velocidade_padrao = velocidade_padrao
        self.velocidade = self.velocidade_padrao
        self.raio = 100 # caso o raio do dragão for diferente do raio dos outros animais, talvez exista um problema na colisão entre eles
        self.vida = vida
        self.direcao = False
        self.repouso = 0
        self.mago = instancia_mago
        Dragao.dragoes_vivos.append(self)

    def spawnar(self, mago, paredes, rios):
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
                for dragao in Dragao.dragoes_vivos:
                    if dragao != self and ((dragao.x + (dragao.largura / 2) - valorx) ** 2 + (dragao.y + (dragao.altura / 2) - valory)** 2) ** (1/2) < dragao.raio:
                        escolher = False
                bloqueio = []
                for k in paredes:
                    bloqueio.append(k)
                for k in rios:
                    bloqueio.append(k)
                for bloqueador in bloqueio:
                    if colisao_amigavel(self, bloqueador):
                        escolher = False

    def desenhar_dragao(self, janela):
        # Falta adicionar imagens/animações do dragão
        dragao_imagem = pg.transform.smoothscale(pg.image.load('assets/lobo.png'), (50,50))
        
        if self.direcao == 'direita' or self.direcao == False: # O dragão sendo inicialmente desenhado para o lado direito
            janela.blit(dragao_imagem, (self.x, self.y))
        elif self.direcao == 'esquerda':
            janela.blit(dragao_imagem, (self.x, self.y))
        elif self.direcao == 'cima':
            janela.blit(dragao_imagem, (self.x, self.y))
        elif self.direcao == 'baixo':
            janela.blit(dragao_imagem, (self.x, self.y))

    def morte(self):
        Dragao.dragoes_vivos.remove(self)
    
    def move(self, mago, variacao_tempo, paredes, rios, velocidade_devagar, velocidade_rapida):
        raio_alerta = mago.raio
        if mago.velocidade == velocidade_rapida:
            raio_alerta = raio_alerta * 1.5
        elif mago.velocidade == velocidade_devagar:
            raio_alerta = raio_alerta / 1.5
        distancia_x = mago.x - self.x
        distancia_y = mago.y - self.y
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
        for k in Dragao.dragoes_vivos:
            if k != self:
                bloqueio.append(k)
        for k in paredes:
            bloqueio.append(k)
        for k in rios:
            bloqueio.append(k)
        for dragao in bloqueio:
            if colisao_amigavel(self, dragao):
                self.x = antigo_x
                self.y = antigo_y
