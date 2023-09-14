import pygame as pg
from .utilidades import AMARELO

class Projectile(object):
    def __init__(self,x,y,radius,facing_x, facing_y):
        self.largura = 10
        self.altura = 10
        self.x = x
        self.y = y
        self.cor = AMARELO
        self.radius = radius
        self.facing_x = facing_x
        self.facing_y = facing_y
        self.vel_x = 8 * facing_x
        self.vel_y = 8 * facing_y
        
    def draw(self,janela):
        projetil = pg.transform.smoothscale(pg.image.load('assets/projetil.png'), (10,10))
        janela.blit(projetil, (self.x, self.y))
