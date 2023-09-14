import pygame as pg

class Projectile(object):
    def __init__(self,x,y,radius,facing_x, facing_y):
        self.largura = 50
        self.altura = 50
        self.x = x
        self.y = y
        self.radius = radius
        self.facing_x = facing_x
        self.facing_y = facing_y
        self.vel_x = 4 * facing_x
        self.vel_y = 4 * facing_y
        
        if self.facing_x == 1:
            self.y -= 30
        if self.facing_x == -1:
            self.x -= 30
            self.y -= 30
        if self.facing_y == -1:
            self.y -= 30
        if self.facing_y == 1:
            self.x -= 30
            self.y -= 30

    def draw(self,janela):
        projetil_padrao = pg.transform.smoothscale(pg.image.load('assets/projetil.png'), (50,30))
        projetil_left = pg.transform.flip(pg.transform.smoothscale(pg.image.load('assets/projetil.png'), (50,30)), True, False) #espelha a imagem
        projetil_up = pg.transform.rotate(pg.transform.smoothscale(pg.image.load('assets/projetil.png'), (50,30)), 90) #rotaciona a imagem
        projetil_down = pg.transform.rotate(pg.transform.smoothscale(pg.image.load('assets/projetil.png'), (50,30)), 270) #rotaciona a imagem

        if self.facing_x == 1:
            janela.blit(projetil_padrao, (self.x, self.y))
        if self.facing_x == -1:
            janela.blit(projetil_left, (self.x, self.y))
        if self.facing_y == -1:
            janela.blit(projetil_up, (self.x, self.y))
        if self.facing_y == 1:
            janela.blit(projetil_down, (self.x, self.y))
