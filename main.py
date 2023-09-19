import pygame as pg
import sys
import time
import random
from classes import Inimigos, Parede, Retangulo, Rio, Projectile, Lobo

#Imagens
hud = pg.transform.scale(pg.image.load('assets/hud.png'), (1800, 60)) #imagem da madeira do menu inferior

#animal1
animal1_baixo = pg.transform.smoothscale(pg.image.load('assets/animal1_frente.png'), (50, 50))
animal1_cima = pg.transform.smoothscale(pg.image.load('assets/animal1_costas.png'), (50, 50))
animal1_direita = pg.transform.smoothscale(pg.image.load('assets/animal1_direita.png'), (50, 50))
animal1_esquerda = pg.transform.flip(animal1_direita, True, False)

#animal2
animal2_baixo = pg.transform.smoothscale(pg.image.load('assets/animal2_frente.png'), (50, 50))
animal2_cima = pg.transform.smoothscale(pg.image.load('assets/animal2_costas.png'), (50, 50))
animal2_direita = animal2_baixo
animal2_esquerda = animal2_cima

#animal3
animal3 = pg.transform.smoothscale(pg.image.load('assets/animal3.png'), (50, 50))
animal3_direita = animal3
animal3_esquerda = animal3
animal3_cima = animal3
animal3_baixo = animal3

# Colisão com as bordas
def borda(variavel, width, height):
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
    if player.x + player.largura >= objeto.x >= player.x or objeto.x + objeto.largura >= player.x >= objeto.x:
        if player.y + player.altura >= objeto.y >= player.y or objeto.y + objeto.altura >= player.y >= objeto.y:
            objeto.morte()
            pontos_inimigos[objeto.nome] += 1

def colisao_lobo(player, objeto):
    if player.x + player.largura >= objeto.x >= player.x or objeto.x + objeto.largura >= player.x >= objeto.x:
        if player.y + player.altura >= objeto.y >= player.y or objeto.y + objeto.altura >= player.y >= objeto.y:
            objeto.morte()

def colisao_amigavel(objeto1, objeto2):
    if (objeto2.x + objeto2.largura >= objeto1.x >= objeto2.x or objeto1.x + objeto1.largura >= objeto2.x >= objeto1.x) and (objeto2.y + objeto2.altura >= objeto1.y >= objeto2.y or objeto1.y + objeto1.altura >= objeto2.y >= objeto1.y):
        return True

# Verifica se o lobo entra em contato com o mago e dá dano no mago
def dano_lobo(mago, lobo):
    if mago.x + mago.largura >= lobo.x >= mago.x or mago.x + mago.largura >= lobo.x + lobo.largura >= mago.x:
        if mago.y + mago.altura >= lobo.y >= mago.y or mago.y + mago.altura >= lobo.y + lobo.altura >= mago.y:
            mago.vida -= 10
            if mago.vida <= 0:
                mago.vida = 0
            lobo.velocidade = 0

#cria as bordas do rio
def contorno_rio(mapa, x_vez, y_vez):
    if (x_vez, y_vez + 100) in mapa.keys():
        if mapa[(x_vez, y_vez + 100)] != 14 and mapa[(x_vez, y_vez + 100)] != 15:
            if mapa[(x_vez, y_vez + 100)] == 17:
                mapa[(x_vez, y_vez + 100)] = 20
            else:
                mapa[(x_vez, y_vez + 100)] = 16
            if (x_vez + 50, y_vez + 100) in mapa.keys():
                if mapa[(x_vez + 50, y_vez + 100)] == 19:
                    mapa[(x_vez + 50, y_vez + 100)] = 23
                else:
                    mapa[(x_vez + 50, y_vez + 100)] = 16
    if (x_vez + 100, y_vez) in mapa.keys():
        if mapa[(x_vez + 100, y_vez)] != 14 and mapa[(x_vez + 100, y_vez)] != 15:
            if  mapa[(x_vez + 100, y_vez)] == 16:
                mapa[(x_vez + 100, y_vez)] = 20
            else:
                mapa[(x_vez + 100, y_vez)] = 17   
    if (x_vez + 100, y_vez + 50) in mapa.keys():
        if mapa[(x_vez + 100, y_vez + 50)] != 14 and mapa[(x_vez + 100, y_vez + 50)] != 15:
            if mapa[(x_vez + 100, y_vez + 50)] == 18:
                mapa[(x_vez + 100, y_vez + 50)] = 21
            else:
                mapa[(x_vez + 100, y_vez + 50)] = 17
    if (x_vez, y_vez - 50) in mapa.keys():
        if mapa[(x_vez, y_vez - 50)] != 14 and mapa[(x_vez, y_vez - 50)] != 15:
            if mapa[(x_vez, y_vez - 50)] == 17:
                mapa[(x_vez, y_vez - 50)] = 21
            else:
                mapa[(x_vez, y_vez - 50)] = 18
    if (x_vez + 50, y_vez - 50) in mapa.keys():
        if mapa[(x_vez + 50, y_vez - 50)] != 14 and mapa[(x_vez + 50, y_vez - 50)] != 15:
            if mapa[(x_vez + 50, y_vez - 50)] == 19:
                mapa[(x_vez + 50, y_vez - 50)] = 22
            else:
                mapa[(x_vez + 50, y_vez - 50)] = 18
    if (x_vez - 50, y_vez) in mapa.keys():
        if mapa[(x_vez - 50, y_vez)] != 14 and mapa[(x_vez - 50, y_vez)] != 15:
            if mapa[(x_vez - 50, y_vez)] == 16:
                mapa[(x_vez - 50, y_vez)] = 23
            else:
                mapa[(x_vez - 50, y_vez)] = 19
    if (x_vez -50, y_vez + 50) in mapa.keys():
        if mapa[(x_vez -50, y_vez + 50)] != 14 and mapa[(x_vez -50, y_vez + 50)] != 15:
            if mapa[(x_vez -50, y_vez + 50)] == 18:
                mapa[(x_vez -50, y_vez + 50)] = 22
            else:
                mapa[(x_vez -50, y_vez + 50)] = 19
    
pg.init()

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

# Configurações da janela
LARGURA = 1280
ALTURA = 720
janela = pg.display.set_mode((LARGURA, ALTURA))
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
        "Animal 1": {'velocidade': velocidade_devagar, 'referencia': {'esquerda': animal1_esquerda, 'direita' : animal1_direita, 'cima' : animal1_cima, 'baixo' : animal1_baixo}},
        "Animal 2": {'velocidade': velocidade_padrao, 'referencia': {'esquerda': animal2_esquerda, 'direita' : animal2_direita, 'cima' : animal2_cima, 'baixo' : animal2_baixo}},
        "Animal 3": {'velocidade': velocidade_rapida, 'referencia': {'esquerda': animal3_esquerda, 'direita' : animal3_direita, 'cima' : animal3_cima, 'baixo' : animal3_baixo}}
    }

stamina_padrao = 1000
cooldown_habilidade_padrao = 270
vida_padrao = 1000

ponto_inicial = (100, 100)


setas = {'RIGHT': 0, 'LEFT': 0, 'UP': 0, 'DOWN': 0}
ultima_seta = {'RIGHT': 0, 'LEFT': 0, 'UP': 0, 'DOWN': 0, 'SPACE': 0}


#gera cada pequeno pedaço de grama do mapa
tilemap = []
mapa = {}
desenho_enfeites = []
enfeites = {}

#desenho dos detalhes no mapa
num_tiles = 31
num_enfeites = 11
for i in range(num_tiles):
    tilemap.append(pg.transform.scale(pg.image.load(f'assets/tile{i + 1}.png'), (50, 50)))
for j in range(num_enfeites):
    desenho_enfeites.append(pg.transform.scale(pg.image.load(f'assets/enfeite{j + 1}.png'), (50, 50)))
for x in range(0, LARGURA, 50):
    for y in range(0, ALTURA, 50):
        aleatorio = random.randint(1,10)
        if aleatorio == 1:
            numero = random.randint(2, 13)
        else:
            numero = 1
        mapa[(x, y)] = numero


direcoes = ['direita', 'esquerda', 'baixo', 'cima']
direcoes2 = direcoes.copy()
foz = False
direcao_rio_inicial = random.choice(direcoes)
direcoes2.pop(direcoes.index(direcao_rio_inicial))
direcao_rio_final = random.choice(direcoes2)
fluxo_rio = [direcao_rio_inicial, direcao_rio_final]
direcao_rio = direcao_rio_inicial
if ('direita' in fluxo_rio and 'esquerda' in fluxo_rio) or ('cima' in fluxo_rio and 'baixo' in fluxo_rio):
    fluxo_rio = direcoes
    fluxo_rio.remove(direcao_rio_final)

if direcao_rio_inicial == 'direita':
    y = random.randrange(0, ALTURA, 100)
    mapa[(0, y)] = mapa[(50, y)] = mapa[(0, y + 50)] = mapa[(50, y + 50)] = 14
    x_vez = 0
    y_vez = y
elif direcao_rio_inicial == 'esquerda':
    y = random.randrange(0, ALTURA, 100)
    ultimo = LARGURA
    while ultimo % 50 != 0:
        ultimo -= 1
    ultimo -= 50
    mapa[(ultimo, y)] = mapa[(ultimo + 50, y)] = mapa[(ultimo, y + 50)] = mapa[(ultimo + 50, y + 50)] = 14
    x_vez = ultimo
    y_vez = y
elif direcao_rio_inicial == 'baixo':
    x = random.randrange(0, LARGURA, 100)
    mapa[(x, 0)] = mapa[(x, 50)] = mapa[(x + 50, 0)] = mapa[(x + 50, 50)] = 14
    x_vez = x
    y_vez = 0
elif direcao_rio_inicial == 'cima':
    x = random.randrange(0, LARGURA, 100)
    ultimo = ALTURA
    while ultimo % 50 != 0:
        ultimo -= 1
    ultimo -= 50
    mapa[(x, ultimo)] = mapa[(x, ultimo + 50)] = mapa[(x + 50, ultimo)] = mapa[(x + 50, ultimo + 50)] = 14
    x_vez = x
    y_vez = ultimo
Rio(x_vez, y_vez)
contorno_rio(mapa, x_vez, y_vez)

while not foz:
    if direcao_rio == direcao_rio_inicial:
        direcao_rio = random.choice(fluxo_rio)
    else:
        direcao_rio = direcao_rio_inicial
    if direcao_rio == 'direita':
        x_vez += 100
        if x_vez + 150 > LARGURA:
                foz = True
        mapa[(x_vez, y_vez)] = mapa[(x_vez, y_vez + 50)] = mapa[(x_vez + 50, y_vez)] = mapa[(x_vez + 50, y_vez + 50)] = 14
    elif direcao_rio == 'esquerda':
        x_vez -= 100
        if x_vez <= 0:
            foz = True
        mapa[(x_vez, y_vez)] = mapa[(x_vez, y_vez + 50)] = mapa[(x_vez + 50, y_vez)] = mapa[(x_vez + 50, y_vez + 50)] = 14
    elif direcao_rio == 'baixo':
        y_vez += 100
        if y_vez + 100 > ALTURA:
            foz = True
        mapa[(x_vez, y_vez)] = mapa[(x_vez, y_vez + 50)] = mapa[(x_vez + 50, y_vez)] = mapa[(x_vez + 50, y_vez + 50)] = 14
    elif direcao_rio == 'cima':
        y_vez -= 100
        if y_vez <= 0:
            foz = True
        mapa[(x_vez, y_vez)] = mapa[(x_vez, y_vez + 50)] = mapa[(x_vez + 50, y_vez)] = mapa[(x_vez + 50, y_vez + 50)] = 14
    contorno_rio(mapa, x_vez, y_vez)
    Rio(x_vez, y_vez)

for x in range(0, LARGURA, 50):
    for y in range(0, ALTURA, 50):
        if mapa[(x, y)] == 1:
            num = random.randint(1, 30)
            if num == 1:
                aleatorio = random.randint(1, 11)
                posicao_x = random.randint(x, x + 25)
                posicao_y = random.randint(y, y + 25)
                enfeites[(x, y)] = (aleatorio, (posicao_x, posicao_y))
        
#cria as bordas abertas do rio
for (x, y) in mapa.keys():
    if (x + 50, y) in mapa.keys() and (x, y + 50) in mapa.keys():
        if mapa[((x + 50, y))] == 18 and mapa[((x, y + 50))] == 19:
            mapa[(x, y)] = 24
            mapa[(x + 50, y + 50)] = 28
    if (x - 50, y) in mapa.keys() and (x, y + 50) in mapa.keys():
        if mapa[((x - 50, y))] == 18 and mapa[((x, y + 50))] == 17:
            mapa[(x, y)] = 25
            mapa[(x - 50, y + 50)] = 31
    if (x + 50, y) in mapa.keys() and (x, y - 50) in mapa.keys():
        if mapa[((x + 50, y))] == 16 and mapa[((x, y - 50))] == 19:
            mapa[(x, y)] = 26
            mapa[(x + 50, y - 50)] = 29
    if (x - 50, y) in mapa.keys() and (x, y - 50) in mapa.keys():
        if mapa[((x - 50, y))] == 16 and mapa[((x, y - 50))] == 17:
            mapa[(x, y)] = 27
            mapa[(x - 50, y - 50)] = 30
#cria o jogador 
retangulo = Retangulo(velocidade_padrao, stamina_padrao, Rio.rios, cooldown_habilidade_padrao, vida_padrao)

#cria as paredes
num_arvores = random.randint(4,8)
for j in range(num_arvores):
    locals()['parede' + str(j)] = Parede(0.05, retangulo, Rio.rios)

# Spawnar os animais, foi escolhido 3, mas pode ser arbitrário
pontos_inimigos = {}
for animal in infos.keys():
    pontos_inimigos[animal] = 0
for i in range(3):
    nome = random.choice([k for k in infos.keys()])
    locals()['inimigo' + str(i)] = Inimigos(infos, nome, retangulo)
    locals()['inimigo' + str(i)].spawnar(retangulo, Parede.paredes, Rio.rios, Lobo.lobos_vivos)


def draw_poder():
    for poder in cargas:
        poder.draw(janela)

cargas = []

vida_lobo = 450
lobo = Lobo(velocidade_padrao, "Lobo", retangulo, vida_lobo)
lobo.spawnar(retangulo, Parede.paredes, Rio.rios)

# Loop principal
running = True

while running:
    # A movimentação é em função do tempo, se rodar muito ciclos ele para e volta dps
    variacao_tempo = clock.tick(30)

    width = pg.display.get_surface().get_width()
    height = pg.display.get_surface().get_height()

    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            running = False

    if ultima_seta['SPACE'] == 0:
        cooldown = False
    
    if not cooldown:
        #checando colisão com animais
        for animal in Inimigos.inimigos_vivos:
            for poder in cargas:
                if poder.x < 1280 and poder.x > -40:
                    poder.x += poder.vel_x
                else:
                    cargas.pop(cargas.index(poder))
                    cooldown = True
                if poder.y < 720 and poder.y > -60:
                    poder.y += poder.vel_y
                else:
                    cargas.pop(cargas.index(poder))
                    cooldown = True
                if colisao_amigavel(poder, animal):
                    colisao(poder, animal)
                    cargas.pop(cargas.index(poder))
                    cooldown = True

        #checando colisão com animais
        for lobo in Lobo.lobos_vivos:
            for poder in cargas:
                if poder.x < 1280 and poder.x > -40:
                    poder.x += poder.vel_x
                else:
                    cargas.pop(cargas.index(poder))
                    cooldown = True
                if poder.y < 720 and poder.y > -60:
                    poder.y += poder.vel_y
                else:
                    cargas.pop(cargas.index(poder))
                    cooldown = True
                if colisao_amigavel(poder, lobo):
                    colisao_lobo(poder, lobo)
                    cargas.pop(cargas.index(poder))
                    cooldown = True

        #checando colisão com paredes        
        for parede in Parede.paredes:
            for poder in cargas:
                if poder.x < 1280 and poder.x > -40:
                    poder.x += poder.vel_x
                else:
                    cargas.pop(cargas.index(poder))
                    cooldown = True
                if poder.y < 720 and poder.y > -60:
                    poder.y += poder.vel_y
                else:
                    cargas.pop(cargas.index(poder))
                    cooldown = True
                if colisao_amigavel(poder, parede):
                    cargas.pop(cargas.index(poder))
                    cooldown = True

    keys = pg.key.get_pressed()

    if keys[pg.K_F11] and not tela_cheia:
        janela = pg.display.set_mode((LARGURA, ALTURA), pg.FULLSCREEN)
        tela_cheia = True
    if keys[pg.K_ESCAPE] and tela_cheia:
        janela = pg.display.set_mode((LARGURA, ALTURA))
        tela_cheia = False

    for x in range(0, width, 50):
        for y in range(0, height, 50):
            janela.blit(tilemap[mapa[(x, y)] - 1], (x, y))
    
    for x in range(0, width, 50):
        for y in range(0, height, 50):
            if (x, y) in enfeites.keys():
                janela.blit(desenho_enfeites[enfeites[(x, y)][0] - 1], enfeites[(x, y)][1])
    

    for j in range(num_arvores):
        locals()['parede' + str(j)].desenhar_tronco()

    if not cooldown:
        draw_poder()

    # há uma pequena chance de surgir um animal cada vez que o loop roda
    chance = random.randint(1,400)
    total_vivos = len(Inimigos.inimigos_vivos)
    nenhum = True
    for inimigo in Inimigos.inimigos_vivos:
        if not (inimigo.x < -1 * inimigo.largura or inimigo.x >= width or inimigo.y < -1 * inimigo.altura or inimigo.y > height):
            nenhum = False
    if nenhum or total_vivos == 0 or (chance == 1 and total_vivos <= 20): 
        nome = random.choice([j for j in infos.keys()])
        locals()['inimigo' + str(i)] = Inimigos(infos, nome, retangulo)
        locals()['inimigo' + str(i)].spawnar(retangulo, Parede.paredes, Rio.rios, Lobo.lobos_vivos)
    for inimigo in Inimigos.inimigos_vivos:
        inimigo.desenhar_inimigo(janela)
    
    retangulo.desenhar_mago(janela) #desenhando o mago

    for lobo in Lobo.lobos_vivos: #desenhando o lobo
        lobo.desenhar_lobo(janela)

    for j in range(num_arvores):
        locals()['parede' + str(j)].desenhar_folhas()

    ratio_stamina = retangulo.stamina / 1000
    ratio_habilidade = retangulo.cooldown_habilidade / 270
    ratio_vida = retangulo.vida / 1000

    #lugar de informacões
    janela.blit(hud, (-200, height - 60))


    #Moldura barra de vida
    largura_barra = 200
    altura_barra = 15
    raio_borda = 4
    espessura = 2
    x_barras = width / (LARGURA/10)
    x_barra_habilidade = width / (LARGURA / 270)
    y_barra_stamina = height / (ALTURA/(ALTURA - 28))
    y_barra_vida = height / (ALTURA/(ALTURA - 44))
    
    #Fundo barra de stamina
    pg.draw.rect(janela, CINZA, (x_barras, y_barra_stamina, largura_barra, altura_barra), border_radius=raio_borda)

    #Fundo barra de vida
    pg.draw.rect(janela, CINZA, (x_barras, y_barra_vida, largura_barra, altura_barra), border_radius=raio_borda)

    # Barra de vida
    pg.draw.rect(janela, VERDE, (x_barras, y_barra_vida, largura_barra * ratio_vida, altura_barra), border_radius=raio_borda)
    pg.draw.rect(janela, BRANCO, (x_barras + 1, y_barra_vida, (largura_barra - 2) * ratio_vida, altura_barra - 11), border_radius=raio_borda)
    pg.draw.rect(janela, MARROM_ESCURO, (x_barras, y_barra_vida, largura_barra, altura_barra), espessura, border_radius=raio_borda)

    # Barra de stamina
    pg.draw.rect(janela, AMARELO, (x_barras, y_barra_stamina, largura_barra * ratio_stamina, altura_barra), border_radius=raio_borda)
    pg.draw.rect(janela, MARROM_ESCURO, (x_barras, y_barra_stamina, largura_barra, altura_barra), espessura, border_radius=raio_borda)

    #Barra de habilidade
    pg.draw.rect(janela, AZUL, (x_barra_habilidade, y_barra_vida, (largura_barra - 100) * ratio_habilidade, altura_barra), border_radius=raio_borda)
    pg.draw.rect(janela, BRANCO, (x_barra_habilidade + 1, y_barra_vida, (largura_barra - 100 - 2) * ratio_habilidade, (altura_barra - 11)), border_radius=raio_borda)
    pg.draw.rect(janela, MARROM_ESCURO, (x_barra_habilidade, y_barra_vida, (largura_barra - 100), altura_barra), espessura, border_radius=raio_borda)

    #movimentação dos inimigos
    for inimigo in Inimigos.inimigos_vivos:
        inimigo.move(retangulo, variacao_tempo, Parede.paredes, Rio.rios, Lobo.lobos_vivos, velocidade_devagar, velocidade_rapida)
    # Colisão com as bordas
    retangulo = borda(retangulo, width, height)
    for inimigo in Inimigos.inimigos_vivos: 
        inimigo = colisao(retangulo, inimigo)

    # Movimentação do lobo
    for lobo in Lobo.lobos_vivos:
        lobo.move(retangulo, variacao_tempo, Parede.paredes, Rio.rios, velocidade_devagar, velocidade_rapida)

    # Colisão do lobo com o mago
    for lobo in Lobo.lobos_vivos:  
        lobo = dano_lobo(retangulo, lobo)

    retangulo.move(keys, variacao_tempo, setas, ultima_seta, Parede.paredes, Rio.rios)


    #criação do timer
    tempo_atual = time.time()
    tempo_passado = tempo_atual - comeco_timer
    tempo_restante = max(0, duracao_timer - tempo_passado) #evite com que o timer dê errado quando acabe
    minutos, segundos = divmod(int(tempo_restante), 60) #faz a divisão correta entre minutos e segundos
    texto_timer = fonte_tempo.render(f'Tempo: {minutos:02d}:{segundos:02d}', True, BRANCO) #texto, situação de aparecimento, cor
    janela.blit(texto_timer, (LARGURA - texto_timer.get_width() - 15, ALTURA - 50))
    x_inicial = LARGURA - texto_timer.get_width() - 150

    #Blitando os sprites do animais no contador
    janela.blit(animal1_baixo, (x_inicial - 200, ALTURA - 50))
    janela.blit(animal2_baixo, (x_inicial - 100, ALTURA - 50))
    janela.blit(animal3, (x_inicial, ALTURA - 50))

    for animal in reversed(pontos_inimigos.keys()): #contador dos animais
        if pontos_inimigos[animal] < 10:
            contador = fonte_contador.render(f'x0{pontos_inimigos[animal]}', True, BRANCO)
        else:
            contador = fonte_contador.render(f'x{pontos_inimigos[animal]}', True, BRANCO) 
        janela.blit(contador, (x_inicial + 27, ALTURA - 57))
        x_inicial -= 100
    
    if not cooldown:
        if keys[pg.K_SPACE]:
            if ultima_seta['LEFT'] != 0:
                facing_x = -1
                facing_y = 0
            elif ultima_seta['RIGHT'] != 0:
                facing_x = 1
                facing_y = 0
            elif ultima_seta['UP'] != 0:
                facing_y = -1
                facing_x = 0
            else:
                facing_y = 1
                facing_x = 0


            if len(cargas) < 1:
                cargas.append(Projectile(round(retangulo.x + retangulo.largura //2), round(retangulo.y + retangulo.altura//2), 4, facing_x, facing_y))

    janela.blit(janela, (0,0)) #atualiza o timer e as barras corretamente

    pg.display.update()

# Encerra Pygame
pg.quit()
sys.exit()
