import pygame as pg
import random
from .functions import *
from .projectile import Projectile


class Dragao(pg.sprite.Sprite):
    # Responsável por cada dragão vivo
    dragoes_vivos = []

    def __init__(self, velocidade_padrao, nome, instancia_mago, vida, frames_dragao, frames_poder):
        super().__init__()
        self.largura = 198
        self.altura = 128
        self.nome = nome
        self.velocidade_padrao = velocidade_padrao
        self.velocidade = 0
        self.raio = 600 # caso o raio do dragão for diferente do raio dos outros animais, talvez exista um problema na colisão entre eles
        self.vida = vida
        self.direcao = 'baixo'
        self.esquerda = frames_dragao['Dragao']['referencia']['esquerda']
        self.direita = frames_dragao['Dragao']['referencia']['direita']
        self.cima = frames_dragao['Dragao']['referencia']['cima']
        self.baixo = frames_dragao['Dragao']['referencia']['baixo']
        self.img = self.baixo[0]
        self.repouso = 0
        self.mago = instancia_mago
        self.estagio = 0
        self.estado = 'parado'
        self.frames_poder = frames_poder
        self.cooldown = 0
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

    def desenhar_dragao(self, janela, offset_x, offset_y):
        # Falta adicionar imagens/animações do dragão
        janela.blit(self.img, (self.x - offset_x, self.y - offset_y))

    def morte(self):
        Dragao.dragoes_vivos.remove(self)
    
    def move(self, mago, variacao_tempo, paredes, rios, velocidade_devagar, velocidade_rapida, cargas_dragao):
        raio_alerta = mago.raio
        if mago.velocidade == velocidade_rapida:
            raio_alerta = raio_alerta * 1.5
        elif mago.velocidade == velocidade_devagar:
            raio_alerta = raio_alerta / 1.5
        distancia_x = (mago.x + mago.largura / 2) -  (self.x + self.largura/2)
        distancia_y = (mago.y)  - (self.y + self.altura/ 2)
        antigo_x = self.x
        antigo_y = self.y
        
        if self.estado == 'parado' and ((distancia_x)**2 + (distancia_y)**2)**(1/2) <= raio_alerta:
            if ((abs(distancia_x) > 5 and abs(distancia_y) > 5)):
                self.velocidade = self.velocidade_padrao
                if abs(distancia_x) < abs(distancia_y):
                    if distancia_x < 0:
                        self.direcao = 'esquerda'
                    else:
                        self.direcao = 'direita'
                else:
                    if distancia_y < 0:
                        self.direcao = 'cima'
                    else:
                        self.direcao = 'baixo'
                self.estado = 'andando'
        elif ((distancia_x)**2 + (distancia_y)**2)**(1/2) > raio_alerta:
            self.velocidade = 0
            self.estado = 'parado'
        elif self.estado == 'andando':
            self.velocidade = self.velocidade_padrao
    
        if self.direcao == 'direita':
            self.x += self.velocidade * variacao_tempo
            self.estagio += 0.2
            self.img = self.direita[int(self.estagio % 3)]
        elif self.direcao == 'esquerda':
            self.x -= self.velocidade * variacao_tempo
            self.estagio += 0.2
            self.img = self.esquerda[int(self.estagio % 3)]
        elif self.direcao == 'baixo':
            self.y += self.velocidade * variacao_tempo
            self.estagio += 0.2
            self.img = self.baixo[int(self.estagio % 3)]
        elif self.direcao == 'cima':
            self.y -= self.velocidade * variacao_tempo
            self.estagio += 0.2
            self.img = self.cima[int(self.estagio % 3)]
        if self.estagio == 3:
            self.estagio = 0

        if ((abs(distancia_x) <= 5 or abs(distancia_y) <= 5))and ((distancia_x)**2 + (distancia_y)**2)**(1/2) <= raio_alerta:
            self.estado = 'atirando'
        
        if self.estado == 'atirando':
            self.velocidade = 0
            if abs(distancia_x)  > abs(distancia_y):
                if distancia_x < 0:
                    self.direcao = 'esquerda'
                    facing_x = -1
                    facing_y = 0
                else:
                    self.direcao = 'direita'
                    facing_x = 1
                    facing_y = 0
                if self.cooldown == 0:
                        cargas_dragao.append(Projectile(round(self.x + self.largura //2), round(self.y + self.altura//1.5), 4, facing_x, facing_y, mago.poder, self.frames_poder))
                        self.estado = 'parado'
                        self.cooldown = 50
            else:
                if distancia_y < 0:
                    self.direcao = 'cima'
                    facing_y = -1
                    facing_x = 0
                    if self.cooldown == 0:
                        cargas_dragao.append(Projectile(round(self.x + self.largura //2.5), round(self.y + self.altura//2), 4, facing_x, facing_y, mago.poder, self.frames_poder))
                        self.estado = 'parado'
                        self.cooldown = 50
                else:
                    self.direcao = 'baixo'
                    facing_y = 1
                    facing_x = 0
                    if self.cooldown == 0:
                        cargas_dragao.append(Projectile(round(self.x + self.largura // 2), round(self.y + self.altura//2), 4, facing_x, facing_y, mago.poder, self.frames_poder))
                        self.estado = 'parado'
                        self.cooldown = 50
        
        if self.cooldown > 0:
            self.cooldown -= 1
            
        bloqueio = []
        for k in Dragao.dragoes_vivos:
            if k != self:
                bloqueio.append(k)
        for animal in bloqueio:
            if colisao_amigavel(self, animal):
                self.x = antigo_x
                self.y = antigo_y