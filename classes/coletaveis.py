import pygame as pg
import random
from .utilidades import *

# mesma lógica dos animais, mas sem movimentação
class Coletaveis:
    coletaveis_ativos = []

    def __init__(self, nome):
        self.nome = nome
        self.largura = 50
        self.altura = 50
        self.img = pg.transform.smoothscale(pg.image.load('assets/projetil1_0.png'), (1000, 1000))

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
    
    def tipo_poder(self):
        if self.nome == 'fogo':
            #mudar o lugar de onde o fogo está sendo atirado, não entendo o código
        if self.nome == 'velocidade':
            #reduzir a velocidade, simples
        if self.nome == 'tempo':
            #aumentar o tempo, simples também
        if self.nome == 'vida':
            #aumentar a vida, trivial
            
