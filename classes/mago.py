import pygame as pg
import random

def colisao_amigavel(objeto1, objeto2):
    if (objeto2.x + objeto2.largura >= objeto1.x >= objeto2.x or objeto1.x + objeto1.largura >= objeto2.x >= objeto1.x) and (objeto2.y + objeto2.altura >= objeto1.y >= objeto2.y or objeto1.y + objeto1.altura >= objeto2.y >= objeto1.y):
        return True

LARGURA = 1280
ALTURA = 720
stamina_padrao = 1000

class Mago:
    def __init__(self, velocidade, stamina, rios, cooldown_habilidade, vida):
        w = pg.display.get_surface().get_width()
        h = pg.display.get_surface().get_height()
        self.largura = w / 25.6
        self.altura = h / 14.4
        escolheu = False
        while not escolheu:
            escolheu = True
            self.x = random.randrange(0, LARGURA, 50)
            self.y = random.randrange(100, ALTURA, 50)
            for rio in rios:
                if colisao_amigavel(self, rio):
                    escolheu = False
        self.velocidade = velocidade
        self.stamina = stamina
        self.vida = vida
        self.cooldown_habilidade = cooldown_habilidade
        self.cansaco = 0
        self.img = pg.image.load('assets/mago_down.png')
        self.raio = 300

    def move(self, keys, variacao_tempo, setas, ultima_seta, paredes, rios):
        #método usado pra conferir qual tecla foi usada mais recentemente
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            setas['RIGHT'] += 1
            ultima_seta['RIGHT'] = 1
            ultima_seta['LEFT'] = 0
            ultima_seta['UP'] = 0
            ultima_seta['DOWN'] = 0
        else:
            setas['RIGHT'] = 0
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            setas['LEFT'] += 1
            ultima_seta['RIGHT'] = 0
            ultima_seta['LEFT'] = 1
            ultima_seta['UP'] = 0
            ultima_seta['DOWN'] = 0
        else:
            setas['LEFT'] = 0
        if keys[pg.K_UP] or keys[pg.K_w]:
            setas['UP'] += 1
            ultima_seta['RIGHT'] = 0
            ultima_seta['LEFT'] = 0
            ultima_seta['UP'] = 1
            ultima_seta['DOWN'] = 0
        else:
            setas['UP'] = 0
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            setas['DOWN'] += 1
            ultima_seta['RIGHT'] = 0
            ultima_seta['LEFT'] = 0
            ultima_seta['UP'] = 0
            ultima_seta['DOWN'] = 1
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
                self.img = pg.image.load('assets/mago_right.png')
                self.x += self.velocidade * variacao_tempo
            elif escolhida == 'LEFT':
                self.img = pg.image.load('assets/mago_left.png')
                self.x -= self.velocidade * variacao_tempo
            elif escolhida == 'UP':
                self.img = pg.image.load('assets/mago_up.png')
                self.y -= self.velocidade * variacao_tempo
            elif escolhida == 'DOWN':
                self.img = pg.image.load('assets/mago_down.png')
                self.y += self.velocidade * variacao_tempo
            else:
                self.img = pg.image.load('assets/mago_down.png')
        bloqueio = []
        for k in paredes:
            bloqueio.append(k)
        for k in rios:
            bloqueio.append(k)
        for bloqueador in bloqueio:
            if colisao_amigavel(self, bloqueador):
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
        
        if ultima_seta['SPACE'] == 0:
            if keys[pg.K_SPACE]:
                ultima_seta['SPACE'] = 1
                self.cooldown_habilidade = 0
        if ultima_seta['SPACE'] == 1:
            self.cooldown_habilidade += 5
            if self.cooldown_habilidade == 270:
                ultima_seta['SPACE'] = 0

    def desenhar_mago(self, janela):
        escala = 1/4
        imagem = pg.image.load('assets/mago_down.png')
        w, h = imagem.get_size()
        self.largura = w * escala
        # como a imagem do mago é gerada 2/3 abaixo do y dele, a hitbox coincide com sua parte mais inferior
        self.altura = (h * escala) / 3
        redimensionar = pg.transform.smoothscale(self.img, ((w*escala), (h*escala)))
        janela.blit(redimensionar, (self.x, self.y - 2 * self.altura))
