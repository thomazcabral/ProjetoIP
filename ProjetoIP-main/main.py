import pygame as pg
import sys
import time
import random
from classes import Inimigos, Parede, Retangulo


# Colisão com as bordas
def borda(variavel):
    global width
    global height
    if variavel.x < 0:
        variavel.x = 0
    if variavel.x > width - variavel.largura:
        variavel.x = width - variavel.largura
    if variavel.y < 0:
        variavel.y = 0
    if variavel.y > height - variavel.altura - 60:
        variavel.y = height - variavel.altura - 60
    return variavel


# Colisão do player com os animais
def colisao(player, objeto):
    if player.x + player.largura >= objeto.x >= player.x or player.x + player.largura >= objeto.x + objeto.largura >= player.x:
        if player.y + player.altura >= objeto.y >= player.y or player.y + player.altura >= objeto.y + objeto.altura >= player.y:
            objeto.morte()
            pontos_inimigos[objeto.nome] += 1

def colisao_amigavel(objeto1, objeto2):
    if (objeto2.x + objeto2.largura >= objeto1.x >= objeto2.x or objeto1.x + objeto1.largura >= objeto2.x >= objeto1.x) and (objeto2.y + objeto2.altura >= objeto1.y >= objeto2.y or objeto1.y + objeto1.altura >= objeto2.y >= objeto1.y):
        return True

# Colisão do player com os animais
def colisao(player, objeto):
    if player.x + player.largura >= objeto.x >= player.x or player.x + player.largura >= objeto.x + objeto.largura >= player.x:
        if player.y + player.altura >= objeto.y >= player.y or player.y + player.altura >= objeto.y + objeto.altura >= player.y:
            objeto.morte()
            pontos_inimigos[objeto.nome] += 1

pg.init()

BRANCO = (255, 255, 255)
VERDE = (0, 230, 0)
PRETO = (0, 0, 0)
AMARELO = (255, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (95,159,159)
MARROM = (210, 180, 140)
MARROM_ESCURO = (123, 66, 48)
CINZA = (211,211,211)

# Configurações da janela
LARGURA = 1280
ALTURA = 720
janela = pg.display.set_mode((LARGURA, ALTURA))
tela_cheia = False


fonte = pg.font.Font('CW_BITMP.ttf', 24) #fonte importada para o menu inferior
duracao_timer = 60 #em segundos
comeco_timer = time.time() #início do timer
clock = pg.time.Clock()

#velocidade dos animais
velocidade_devagar = 0.05
velocidade_padrao = 0.0575
velocidade_rapida = 0.065


#informações cruciais dos animais
infos = {
        "Animal 1": {'velocidade': velocidade_devagar, 'referencia': AZUL},
        "Animal 2": {'velocidade': velocidade_padrao, 'referencia': VERDE},
        "Animal 3": {'velocidade': velocidade_rapida, 'referencia': VERMELHO}
    }

stamina_padrao = 1000

ponto_inicial = (100, 100)

retangulo = Retangulo(ponto_inicial[0], ponto_inicial[1], velocidade_padrao, stamina_padrao)

#cria as paredes
num_arvores = random.randrange(4,8)
for j in range(num_arvores):
    locals()['parede' + str(j)] = Parede(0.05, retangulo)

# Spawnar os animais, foi escolhido 3 mas é arbitrário

# Spawnar os animais, foi escolhido 3, mas pode ser arbitrário

pontos_inimigos = {}
for animal in infos.keys():
    pontos_inimigos[animal] = 0
for i in range(3):
    nome = random.choice([k for k in infos.keys()])
    locals()['inimigo' + str(i)] = Inimigos(infos, nome, retangulo)
    locals()['inimigo' + str(i)].spawnar(retangulo)

setas = {'RIGHT': 0, 'LEFT': 0, 'UP': 0, 'DOWN': 0} # Status de movimento inicial do retângulo (parado)
# Loop principal
running = True

hud = pg.transform.scale(pg.image.load('hud.png'), (1800, 60)) #imagem da madeira do menu inferior

#gera cada pequeno pedaço de grama do mapa
tilemap = []
mapa = {}
for i in range(13):
    tilemap.append(pg.transform.scale(pg.image.load(f'tile{i + 1}.png'), (50, 50)))
    for x in range(0, LARGURA, 50):
        for y in range(0, ALTURA, 50):
            num1 = random.randrange(1,10)
            if num1 == 1:
                num = random.randrange(1, 13)
            else:
                num = 0
            mapa[(x, y)] = num

while running:

    # A movimentação é em função do tempo, se rodar muito ciclos ele para e volta dps
    variacao_tempo = clock.tick(30)

    width = pg.display.get_surface().get_width()
    height = pg.display.get_surface().get_height()

    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()

    if keys[pg.K_F11] and not tela_cheia:
        janela = pg.display.set_mode((LARGURA, ALTURA), pg.FULLSCREEN)
        tela_cheia = True
    if keys[pg.K_ESCAPE] and tela_cheia:
        janela = pg.display.set_mode((LARGURA, ALTURA))
        tela_cheia = False

    for x in range(0, width, 50):
        for y in range(0, height, 50):
            janela.blit(tilemap[mapa[(x, y)]], (x, y))
    
    for j in range(num_arvores):
        locals()['parede' + str(j)].desenhar_tronco()
    # há uma pequena chance de surgir um animal cada vez que o loop roda

    retangulo.desenhar_mago(janela)

    chance = random.randrange(1,500)
    total_vivos = len(Inimigos.inimigos_vivos)
    if total_vivos == 0 or (chance == 1 and total_vivos <= 20): 
        nome = random.choice([j for j in infos.keys()])
        locals()['inimigo' + str(i)] = Inimigos(infos, nome, retangulo)
        locals()['inimigo' + str(i)].spawnar(retangulo)
    for inimigo in Inimigos.inimigos_vivos:
        inimigo.desenhar_inimigo(janela)
    
    for j in range(num_arvores):
        locals()['parede' + str(j)].desenhar_folhas()
        
    ratio_stamina = retangulo.stamina / 1000
    
    #lugar de informacões
    janela.blit(hud, (-200, height - 60))

    #Moldura barra de vida
    largura_barra = 200
    altura_barra = 15
    raio_borda = 4
    espessura = 2
    x_barras = width / (LARGURA/10)
    y_barra_stamina = height / (ALTURA/(ALTURA - 28))
    y_barra_vida = height / (ALTURA/(ALTURA - 44))
    
    #Fundo barra de stamina
    pg.draw.rect(janela, CINZA, (x_barras, y_barra_stamina, largura_barra, altura_barra), border_radius=raio_borda)

    #Fundo barra de vida
    pg.draw.rect(janela, CINZA, (x_barras, y_barra_vida, largura_barra, altura_barra), border_radius=raio_borda)

    # Barra de vida
    pg.draw.rect(janela, VERDE, (x_barras, y_barra_vida, largura_barra, altura_barra), border_radius=raio_borda)
    pg.draw.rect(janela, MARROM_ESCURO, (x_barras, y_barra_vida, largura_barra, altura_barra), espessura, border_radius=raio_borda)

    # Barra de stamina
    pg.draw.rect(janela, AMARELO, (x_barras, y_barra_stamina, largura_barra * ratio_stamina, altura_barra), border_radius=raio_borda)
    pg.draw.rect(janela, MARROM_ESCURO, (x_barras, y_barra_stamina, largura_barra, altura_barra), espessura, border_radius=raio_borda)


    #movimentação dos inimigos
    for inimigo in Inimigos.inimigos_vivos:
        inimigo.move(retangulo, variacao_tempo)
    # Colisão com as bordas
    retangulo = borda(retangulo)
    for inimigo in Inimigos.inimigos_vivos: 
        inimigo = borda(inimigo)
        inimigo = colisao(retangulo, inimigo)

    retangulo.move(keys, variacao_tempo, setas)

    tempo_atual = time.time()
    tempo_passado = tempo_atual - comeco_timer
    tempo_restante = max(0, duracao_timer - tempo_passado) #evite com que o timer dê errado quando acabe
    minutos, segundos = divmod(int(tempo_restante), 60) #faz a divisão correta entre minutos e segundos
    texto_timer = fonte.render(f'Tempo: {minutos:02d}:{segundos:02d}', True, (0, 0, 0)) #texto, situação de aparecimento, cor
    janela.blit(texto_timer, (LARGURA - texto_timer.get_width() - 15, ALTURA - 50))
    x_inicial = LARGURA - texto_timer.get_width() - 200 
    for animal in reversed(pontos_inimigos.keys()):
        texto_contador = fonte.render(f'{animal}: {pontos_inimigos[animal]}', True, (0, 0, 0)) #contador dos animais
        janela.blit(texto_contador, (x_inicial, ALTURA - 50))
        x_inicial -= 150

    janela.blit(janela, (0,0)) #atualiza o timer e as barras corretamente

    pg.display.update()

# Encerra Pygame
pg.quit()
sys.exit()
