import pygame as pg

def colisao_amigavel(objeto1, objeto2):
    if (objeto2.x + objeto2.largura >= objeto1.x >= objeto2.x or objeto1.x + objeto1.largura >= objeto2.x >= objeto1.x) and (objeto2.y + objeto2.altura >= objeto1.y >= objeto2.y or objeto1.y + objeto1.altura >= objeto2.y >= objeto1.y):
        return True

largura_camera = 1280
altura_camera = 720
janela = pg.display.set_mode((largura_camera, altura_camera))
PRETO = (0, 0, 0)
AMARELO = (255, 255, 0)

stamina_padrao = 1000
cooldown_habilidade_padrao = 270
velocidade_padrao = 0.0575
ponto_inicial = (100, 100)

velocidade_devagar = 0.05
velocidade_rapida = 0.065

setas = {'RIGHT': 0, 'LEFT': 0, 'UP': 0, 'DOWN': 0}
ultima_seta = {'RIGHT': 0, 'LEFT': 0, 'UP': 0, 'DOWN': 0, 'SPACE': 0}
