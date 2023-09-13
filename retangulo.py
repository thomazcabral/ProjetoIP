import pygame as pg

from .parede import Parede

def colisao_amigavel(objeto1, objeto2):
    if (objeto2.x + objeto2.largura >= objeto1.x >= objeto2.x or objeto1.x + objeto1.largura >= objeto2.x >= objeto1.x) and (objeto2.y + objeto2.altura >= objeto1.y >= objeto2.y or objeto1.y + objeto1.altura >= objeto2.y >= objeto1.y):
        return True

LARGURA = 1280
ALTURA = 720
stamina_padrao = 1000

class Retangulo:
    def __init__(self, x, y, velocidade, stamina):
        w = pg.display.get_surface().get_width()
        h = pg.display.get_surface().get_height()
        self.x = x
        self.y = y
        self.largura = w / 25.6
        self.altura = h / 14.4
        self.velocidade = velocidade
        self.stamina = stamina
        self.cansaco = 0
        self.img = pg.image.load('mago_down.png')
        self.raio = 300

    def move(self, keys, variacao_tempo, setas):
        global janela
        #método usado pra conferir qual tecla foi usada mais recentemente
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            setas['RIGHT'] += 1
        else:
            setas['RIGHT'] = 0
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            setas['LEFT'] += 1
        else:
            setas['LEFT'] = 0
        if keys[pg.K_UP] or keys[pg.K_w]:
            setas['UP'] += 1
        else:
            setas['UP'] = 0
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            setas['DOWN'] += 1
        else:
            setas['DOWN'] = 0
        
        vezes = False
        escolhida = False
        for seta in setas.keys():
            if setas[seta] > 0:
                if not vezes or setas[seta] <= vezes:
                    vezes = setas[seta]
                    escolhida = seta
        
        antigo_x = self.x
        antigo_y = self.y
        if escolhida:
            if escolhida == 'RIGHT':
                self.img = pg.image.load('mago_right.png')
                self.x += self.velocidade * variacao_tempo
            elif escolhida == 'LEFT':
                self.img = pg.image.load('mago_left.png')
                self.x -= self.velocidade * variacao_tempo
            elif escolhida == 'UP':
                self.img = pg.image.load('mago_up.png')
                self.y -= self.velocidade * variacao_tempo
            elif escolhida == 'DOWN':
                self.img = pg.image.load('mago_down.png')
                self.y += self.velocidade * variacao_tempo
            else:
                self.img = pg.image.load('mago_down.png')
        global Parede
        for parede in Parede.paredes:
            if colisao_amigavel(self, parede):
                self.x = antigo_x
                self.y = antigo_y
            
        if keys[pg.K_LSHIFT]:
            self.velocidade = 0.05
        if not keys[pg.K_LSHIFT]:
            self.velocidade = 0.1
        if keys[pg.K_LCTRL] and escolhida:
            if self.stamina >= 1 and self.cansaco == 0:
                self.stamina -= 10
                self.velocidade = 0.15
                if self.stamina <= 20:
                    self.cansaco = 200
            elif self.cansaco >= 0:
                self.stamina += 0.65
        elif self.stamina < stamina_padrao:
            self.stamina += 1
        if self.cansaco > 0:
            self.cansaco -= 1
            
    def desenhar_mago(self, janela):
        global width
        global height
        escala = 1/4
        imagem = pg.image.load('mago_down.png')
        w, h = imagem.get_size()
        self.largura = w * escala
        # como a imagem do mago é gerada 2/3 abaixo do y dele, a hitbox coincide com sua parte mais inferior
        self.altura = (h * escala) / 3
        redimensionar = pg.transform.smoothscale(self.img, ((w*escala), (h*escala)))
        janela.blit(redimensionar, (self.x, self.y - 2 * self.altura))