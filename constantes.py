import pygame as pg
import time

pg.init()

#definição de constantes que estavam código principal sem necessidade

#Imagens
hud = pg.transform.scale(pg.image.load('assets/hud.png'), (1800, 60)) #imagem da madeira do menu inferior
hud_skill = pg.transform.smoothscale(pg.image.load('assets/projetil_skill_hud.png'), (64, 48))
hud_skill_cooldown = pg.transform.scale(pg.image.load('assets/projetil_cooldown.png'), (64, 48))

BRANCO = (255, 255, 255)
VERDE = (0, 230, 0)
PRETO = (0, 0, 0)
AMARELO = (255, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (95,159,159)
AZUL_CLARO = (173,216,230)
MARROM = (210, 180, 140)
MARROM_ESCURO = (123, 66, 48)
CINZA = (211,211,211)

LARGURA_MAPA = 1280 * 2
ALTURA_MAPA = 720 * 2
# Configurações da janela
largura_camera = 1280
altura_camera = 720
offset_x = 0
offset_y = 0
janela = pg.display.set_mode((largura_camera, altura_camera))
tela_cheia = False


fonte_contador = pg.font.Font('assets/CW_BITMP.ttf', 18) #fonte importada para o menu inferior
fonte_tempo = pg.font.Font('assets/CW_BITMP.ttf', 24)
duracao_timer = 60 #em segundos
comeco_timer = time.time() #início do timer
clock = pg.time.Clock()

#velocidade dos animais
velocidade_devagar = 0.05
velocidade_padrao = 0.0575
velocidade_rapida = 0.065


#informações cruciais dos animais
infos = {
        "Animal 1": {'velocidade': velocidade_devagar, 'referencia': {}},
        "Animal 2": {'velocidade': velocidade_padrao, 'referencia': {}},
        "Animal 3": {'velocidade': velocidade_rapida, 'referencia': {}}
    }

stamina_padrao = 1000
cooldown_habilidade_padrao = 270
vida_padrao = 1000

ponto_inicial = (100, 100)


setas = {'RIGHT': 0, 'LEFT': 0, 'UP': 0, 'DOWN': 0}
ultima_seta = {'RIGHT': 0, 'LEFT': 0, 'UP': 0, 'DOWN': 0, 'SPACE': 0}
