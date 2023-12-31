import pygame as pg

class Projectile(object):
    def __init__(self,x,y,radius,facing_x, facing_y, nome, frames):
        self.largura = 50
        self.altura = 50
        self.x = x
        self.y = y
        self.radius = radius
        self.facing_x = facing_x
        self.facing_y = facing_y
        self.vel_x = 12.5 * facing_x
        self.vel_y = 10 * facing_y
        self.frames = frames
        self.estagio = 0
        self.nome = nome
        
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

    def draw(self, janela, offset_x, offset_y):
        projetil_padrao = pg.transform.scale(self.frames[self.estagio], (70,40))
        projetil_left = pg.transform.flip(projetil_padrao, True, False) #espelha a imagem
        projetil_down = pg.transform.rotate(projetil_padrao, 270) #rotaciona a imagem
        projetil_up = pg.transform.rotate(projetil_padrao, 90) #rotaciona a imagem 

        if self.facing_x == 1:
            janela.blit(projetil_padrao, (self.x - offset_x, self.y - offset_y))
        if self.facing_x == -1:
            janela.blit(projetil_left, (self.x - offset_x, self.y - offset_y))
        if self.facing_y == -1:
            janela.blit(projetil_up, (self.x - offset_x, self.y - offset_y))
        if self.facing_y == 1:
            janela.blit(projetil_down, (self.x - offset_x, self.y - offset_y))

        self.estagio += 1
        if self.estagio == len(self.frames):
            self.estagio = 0

class Projectile_hud(object):
    def __init__(self, nome, frames):
        self.largura = 50
        self.altura = 50
        self.frames = frames
        self.estagio = 0
        self.nome = nome

    def hud_draw(self, janela):
        projetil_padrao = pg.transform.scale(self.frames[self.estagio], (80,50))

        janela.blit(projetil_padrao, (387, 672))

        self.estagio += 1
        if self.estagio == len(self.frames):
            self.estagio = 0