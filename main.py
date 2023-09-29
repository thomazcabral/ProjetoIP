import pygame as pg
import sys
import time
import random
from classes.utilidades import *
from classes import Animais, Parede, Mago, Rio, Projectile, Dragao, functions, Menu

#Imagens
hud = pg.transform.scale(pg.image.load('assets/hud.png'), (1800, 60)) #imagem da madeira do menu inferior
hud_skill = pg.transform.smoothscale(pg.image.load('assets/projetil_skill_hud.png'), (64, 48))
hud_skill_cooldown = pg.transform.scale(pg.image.load('assets/projetil_cooldown.png'), (64, 48))
    
pg.init()

menu = Menu()

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

#animal
num_animais = 3
num_frames = 3
for k in range(num_animais):
    direita = []
    esquerda = []
    cima = []
    baixo = []
    for i in range(num_frames):
        baixo.append(pg.transform.smoothscale(pg.image.load(f'assets/animal{k + 1}_baixo{i + 1}.png'), (50, 50)))
        cima.append(pg.transform.smoothscale(pg.image.load(f'assets/animal{k + 1}_cima{i + 1}.png'), (37, 55)))
        direita.append(pg.transform.smoothscale(pg.image.load(f'assets/animal{k + 1}_direita{i + 1}.png'), (55, 55)))
        esquerda.append(pg.transform.smoothscale(pg.image.load(f'assets/animal{k + 1}_esquerda{i + 1}.png'), (55, 55)))
    infos[f'Animal {k + 1}']['referencia']['esquerda'] = esquerda
    infos[f'Animal {k + 1}']['referencia']['direita'] = direita
    infos[f'Animal {k + 1}']['referencia']['cima'] = cima
    infos[f'Animal {k + 1}']['referencia']['baixo'] = baixo

animal1_idle =  infos['Animal 1']['referencia']['baixo'][0]
animal2_idle =  infos['Animal 2']['referencia']['baixo'][0]
animal3_idle =  infos['Animal 3']['referencia']['baixo'][0]

frames_dragao = {
    "Dragao": {'referencia': {}},
}

direita_dragao = []
esquerda_dragao = []
cima_dragao = []
baixo_dragao = []
for i in range(num_frames):
    baixo_dragao.append(pg.transform.smoothscale(pg.image.load(f'assets/dragao_baixo_{i + 1}.png'), (198, 128)))
    cima_dragao.append(pg.transform.smoothscale(pg.image.load(f'assets/dragao_cima_{i + 1}.png'), (198, 128)))
    direita_dragao.append(pg.transform.smoothscale(pg.image.load(f'assets/dragao_direita_{i + 1}.png'), (198, 128)))
    esquerda_dragao.append(pg.transform.smoothscale(pg.image.load(f'assets/dragao_esquerda_{i + 1}.png'), (198, 128)))

frames_dragao['Dragao']['referencia']['baixo'] = baixo_dragao
frames_dragao['Dragao']['referencia']['cima'] = cima_dragao
frames_dragao['Dragao']['referencia']['direita'] = direita_dragao
frames_dragao['Dragao']['referencia']['esquerda'] = esquerda_dragao


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
num_tiles = 35
num_enfeites = 11
for i in range(num_tiles):
    tilemap.append(pg.transform.scale(pg.image.load(f'assets/tile{i + 1}.png'), (50, 50)))
for j in range(num_enfeites):
    desenho_enfeites.append(pg.transform.scale(pg.image.load(f'assets/enfeite{j + 1}.png'), (50, 50)))
for x in range(0, LARGURA_MAPA, 50):
    for y in range(0, ALTURA_MAPA, 50):
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
direcao_rio = direcao_rio_inicial

if direcao_rio_inicial == 'direita':
    y = random.randrange(0, ALTURA_MAPA, 100)
    if y > (ALTURA_MAPA / 2):
        direcao_rio_final = 'cima'
    else:
        direcao_rio_final = 'baixo'
    mapa[(0, y)] = mapa[(50, y)] = mapa[(0, y + 50)] = mapa[(50, y + 50)] = 14
    x_vez = 0
    y_vez = y
elif direcao_rio_inicial == 'esquerda':
    y = random.randrange(0, ALTURA_MAPA, 100)
    if y > (ALTURA_MAPA / 2):
        direcao_rio_final = 'cima'
    else:
        direcao_rio_final = 'baixo'
    ultimo = LARGURA_MAPA
    while ultimo % 50 != 0:
        ultimo -= 1
    ultimo -= 50
    mapa[(ultimo, y)] = mapa[(ultimo + 50, y)] = mapa[(ultimo, y + 50)] = mapa[(ultimo + 50, y + 50)] = 14
    x_vez = ultimo
    y_vez = y
elif direcao_rio_inicial == 'baixo':
    x = random.randrange(0, LARGURA_MAPA, 100)
    if x > (LARGURA_MAPA / 2):
        direcao_rio_final = 'esquerda'
    else:
        direcao_rio_final = 'direita'
    mapa[(x, 0)] = mapa[(x, 50)] = mapa[(x + 50, 0)] = mapa[(x + 50, 50)] = 14
    x_vez = x
    y_vez = 0
elif direcao_rio_inicial == 'cima':
    x = random.randrange(0, LARGURA_MAPA, 100)
    if x > (LARGURA_MAPA / 2):
        direcao_rio_final = 'esquerda'
    else:
        direcao_rio_final = 'direita'
    ultimo = ALTURA_MAPA
    while ultimo % 50 != 0:
        ultimo -= 1
    ultimo -= 50
    mapa[(x, ultimo)] = mapa[(x, ultimo + 50)] = mapa[(x + 50, ultimo)] = mapa[(x + 50, ultimo + 50)] = 14
    x_vez = x
    y_vez = ultimo
fluxo_rio = [direcao_rio_inicial, direcao_rio_final]
Rio(x_vez, y_vez)
functions.contorno_rio(mapa, x_vez, y_vez)

while not foz:
    direcao_rio = random.choice(fluxo_rio)
    if direcao_rio == 'direita':
        x_vez += 100
        if x_vez + 150 > LARGURA_MAPA:
                foz = True
        mapa[(x_vez, y_vez)] = mapa[(x_vez, y_vez + 50)] = mapa[(x_vez + 50, y_vez)] = mapa[(x_vez + 50, y_vez + 50)] = 14
    elif direcao_rio == 'esquerda':
        x_vez -= 100
        if x_vez <= 0:
            foz = True
        mapa[(x_vez, y_vez)] = mapa[(x_vez, y_vez + 50)] = mapa[(x_vez + 50, y_vez)] = mapa[(x_vez + 50, y_vez + 50)] = 14
    elif direcao_rio == 'baixo':
        y_vez += 100
        if y_vez + 100 > ALTURA_MAPA:
            foz = True
        mapa[(x_vez, y_vez)] = mapa[(x_vez, y_vez + 50)] = mapa[(x_vez + 50, y_vez)] = mapa[(x_vez + 50, y_vez + 50)] = 14
    elif direcao_rio == 'cima':
        y_vez -= 100
        if y_vez <= 0:
            foz = True
        mapa[(x_vez, y_vez)] = mapa[(x_vez, y_vez + 50)] = mapa[(x_vez + 50, y_vez)] = mapa[(x_vez + 50, y_vez + 50)] = 14
    functions.contorno_rio(mapa, x_vez, y_vez)
    Rio(x_vez, y_vez)


for x in range(0, LARGURA_MAPA, 50):
    for y in range(0, ALTURA_MAPA, 50):
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
mago = Mago(velocidade_padrao, stamina_padrao, Rio.rios, cooldown_habilidade_padrao, vida_padrao)

#cria as paredes
num_arvores = random.randint(10, 30)
for j in range(num_arvores):
    locals()['parede' + str(j)] = Parede(0.05, mago, Rio.rios, LARGURA_MAPA, ALTURA_MAPA)

#cria a ponte
ponte = False
while not ponte:
    bloco = random.choice(Rio.rios)
    if (bloco.x - 100, bloco.y) in mapa.keys() and (bloco.x + 100, bloco.y) in mapa.keys():
        if mapa[(bloco.x - 100, bloco.y)] != 14 and mapa[(bloco.x + 100, bloco.y)] != 14:
            bloco.construir_ponte(mapa)
            ponte = True
            
# Spawnar os animais, foi escolhido 3, mas pode ser arbitrário
pontos_animais = {}
for animal in infos.keys():
    pontos_animais[animal] = 0
for i in range(3):
    nome = random.choice([k for k in infos.keys()])
    locals()['animal' + str(i)] = Animais(infos, nome, mago)
    locals()['animal' + str(i)].spawnar(mago, Parede.paredes, Rio.rios, Dragao.dragoes_vivos, offset_x, offset_y)

#Poderes
poderes = {}
num_frames_poder = 15
tipos_poder = 1
for k in range(tipos_poder):
    frames_poder = []
    for i in range(num_frames_poder):
        frames_poder.append(pg.image.load(f'assets/projetil{k + 1}_{i}.png'))
    poderes[f'poder{k + 1}'] = frames_poder

cargas = []

vida_dragao = 450
dragao = Dragao(velocidade_padrao, "Dragao", mago, vida_dragao, frames_dragao)
dragao.spawnar(mago, Parede.paredes, Rio.rios)

# Loop principal
running = True
game_started = False

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    if not game_started:
        # Mostrar janela do menu
        menu.show_menu(janela)

        # Checar se o jogo deve iniciar
        if menu.start_game:
            game_started = True  # Iniciou

    else:
        # A movimentação é em função do tempo, se rodar muito ciclos ele para e volta dps
        variacao_tempo = clock.tick(30)

        largura_camera = pg.display.get_surface().get_width()
        offset_x = mago.x - (largura_camera / 2)
        if offset_x < 0:
            offset_x = 0
        elif offset_x + (largura_camera) > LARGURA_MAPA:
            offset_x = LARGURA_MAPA - largura_camera
        offset_y = mago.y - (altura_camera / 2)
        if offset_y < 0:
            offset_y = 0
        elif offset_y + (altura_camera) > ALTURA_MAPA:
            offset_y = ALTURA_MAPA - altura_camera
        altura_camera = pg.display.get_surface().get_height()

        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                running = False

        if ultima_seta['SPACE'] == 0:
            cooldown = False
            cooldown_sprite = False
        else:
            cooldown_sprite = True
        
        if not cooldown:
            #checando colisão com animais
            for animal in Animais.animais_vivos:
                for poder in cargas:
                    if offset_x - 40 <= poder.x < largura_camera + offset_x:
                        poder.x += poder.vel_x
                    else:
                        cargas.pop(cargas.index(poder))
                        cooldown = True
                    if offset_y - 60 <= poder.y < altura_camera + offset_y:
                        poder.y += poder.vel_y
                    else:
                        cargas.pop(cargas.index(poder))
                        cooldown = True
                    if functions.colisao_amigavel(poder, animal):
                        functions.colisao(poder, animal, pontos_animais)
                        cargas.pop(cargas.index(poder))
                        cooldown = True

            #checando colisão com animais
            for dragao in Dragao.dragoes_vivos:
                for poder in cargas:
                    if offset_x - 40 <= poder.x < largura_camera + offset_x:
                        poder.x += poder.vel_x
                    else:
                        cargas.pop(cargas.index(poder))
                        cooldown = True
                    if offset_y - 60 <= poder.y < altura_camera + offset_y:
                        poder.y += poder.vel_y
                    else:
                        cargas.pop(cargas.index(poder))
                        cooldown = True
                    if functions.colisao_amigavel(poder, dragao):
                        functions.colisao_dragao(poder, dragao)
                        cargas.pop(cargas.index(poder))
                        cooldown = True

            #checando colisão com paredes        
            for parede in Parede.paredes:
                for poder in cargas:
                    if offset_x - 40 <= poder.x < largura_camera + offset_x:
                        poder.x += poder.vel_x
                    else:
                        cargas.pop(cargas.index(poder))
                        cooldown = True
                    if offset_y - 60 <= poder.y < altura_camera + offset_y:
                        poder.y += poder.vel_y
                    else:
                        cargas.pop(cargas.index(poder))
                        cooldown = True
                    if functions.colisao_amigavel(poder, parede):
                        cargas.pop(cargas.index(poder))
                        cooldown = True

        keys = pg.key.get_pressed()

        if keys[pg.K_F11] and not tela_cheia:
            janela = pg.display.set_mode((largura_camera, altura_camera), pg.FULLSCREEN)
            tela_cheia = True
        if keys[pg.K_ESCAPE] and tela_cheia:
            janela = pg.display.set_mode((largura_camera, altura_camera))
            tela_cheia = False

        for x in range(0, LARGURA_MAPA, 50):
            for y in range(0, ALTURA_MAPA, 50):
                janela.blit(tilemap[mapa[(x, y)] - 1], (x - offset_x, y - offset_y))
        
        for x in range(0, LARGURA_MAPA, 50):
            for y in range(0, ALTURA_MAPA, 50):
                if (x, y) in enfeites.keys():
                    janela.blit(desenho_enfeites[enfeites[(x, y)][0] - 1], (enfeites[(x, y)][1][0] - offset_x, enfeites[(x, y)][1][1] - offset_y))
        

        for j in range(num_arvores):
            locals()['parede' + str(j)].desenhar_tronco(offset_x, offset_y)

        if not cooldown:
            functions.draw_poder(cargas, janela, offset_x, offset_y)

        # há uma pequena chance de surgir um animal cada vez que o loop roda
        chance = random.randint(1,400)
        total_vivos = len(Animais.animais_vivos)
        nenhum = True
        for animal in Animais.animais_vivos:
            if not (animal.x < offset_x -  animal.largura or animal.x >= offset_x + largura_camera or animal.y < offset_y - animal.altura or animal.y > offset_y + altura_camera):
                nenhum = False
        if nenhum or total_vivos == 0 or (chance == 1 and total_vivos <= 20): 
            nome = random.choice([j for j in infos.keys()])
            locals()['animal' + str(i)] = Animais(infos, nome, mago)
            locals()['animal' + str(i)].spawnar(mago, Parede.paredes, Rio.rios, Dragao.dragoes_vivos, offset_x, offset_y)
        for animal in Animais.animais_vivos:
            animal.desenhar_animal(janela, offset_x, offset_y)
        
        mago.desenhar_mago(janela, offset_x, offset_y) #desenhando o mago

        for j in range(num_arvores):
            locals()['parede' + str(j)].desenhar_folhas(offset_x, offset_y)

        for dragao in Dragao.dragoes_vivos: #desenhando o dragao
            dragao.desenhar_dragao(janela, offset_x, offset_y)
            
        ratio_stamina = mago.stamina / 1000
        ratio_habilidade = mago.cooldown_habilidade / 270
        ratio_vida = mago.vida / 1000

        #lugar de informacões
        janela.blit(hud, (-200, altura_camera - 60))


        #Moldura barras
        largura_barra = 200
        largura_barra_skill = 64
        altura_barra = 15
        altura_barra_habilidade = 48
        raio_borda = 4
        espessura = 2
        x_barras = largura_camera / (largura_camera/10)
        y_barra_stamina = altura_camera / (altura_camera/(altura_camera - 28))
        y_barra_vida = altura_camera / (altura_camera/(altura_camera - 44))
        x_barra_habilidade = largura_camera / (largura_camera / 270)
        y_barra_habilidade = y_barra_vida - 9
        
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
        if not cooldown_sprite:
            janela.blit(hud_skill, (x_barra_habilidade, y_barra_habilidade))
        else:
            barra_branca = pg.transform.smoothscale(pg.image.load('assets/barra_branca.png'), (64 * ratio_habilidade, 48))
            barra_branca.set_alpha(100)
            janela.blit(hud_skill_cooldown, (x_barra_habilidade, y_barra_habilidade - 1))
            janela.blit(barra_branca, (x_barra_habilidade, y_barra_habilidade))
        pg.draw.rect(janela, MARROM_ESCURO, (x_barra_habilidade, y_barra_habilidade, largura_barra_skill, altura_barra_habilidade), espessura, border_radius=raio_borda)

        #movimentação dos animais
        for animal in Animais.animais_vivos:
            animal.move(mago, variacao_tempo, Parede.paredes, Rio.rios, Dragao.dragoes_vivos, velocidade_devagar, velocidade_rapida)
        # Colisão com as bordas
        mago = functions.borda(mago, LARGURA_MAPA, ALTURA_MAPA)
        for animal in Animais.animais_vivos: 
            animal = functions.colisao(mago, animal, pontos_animais)

        # Movimentação do dragao
        for dragao in Dragao.dragoes_vivos:
            dragao.move(mago, variacao_tempo, Parede.paredes, Rio.rios, velocidade_devagar, velocidade_rapida)

        # Colisão do dragao com o mago
        for dragao in Dragao.dragoes_vivos:  
            dragao = functions.dano_dragao(mago, dragao)

        mago.move(keys, variacao_tempo, setas, ultima_seta, Parede.paredes, Rio.rios)


        #criação do timer
        tempo_atual = time.time()
        tempo_passado = tempo_atual - comeco_timer
        tempo_restante = max(0, duracao_timer - tempo_passado) #evite com que o timer dê errado quando acabe
        minutos, segundos = divmod(int(tempo_restante), 60) #faz a divisão correta entre minutos e segundos
        texto_timer = fonte_tempo.render(f'Tempo: {minutos:02d}:{segundos:02d}', True, BRANCO) #texto, situação de aparecimento, cor
        janela.blit(texto_timer, (largura_camera - texto_timer.get_width() - 15, altura_camera - 50))
        x_inicial = largura_camera - texto_timer.get_width() - 150

        #Blitando os sprites do animais no contador
        janela.blit(animal1_idle, (x_inicial - 200, altura_camera - 50))
        janela.blit(animal2_idle, (x_inicial - 100, altura_camera - 50))
        janela.blit(animal3_idle, (x_inicial, altura_camera - 50))

        for animal in reversed(pontos_animais.keys()): #contador dos animais
            if pontos_animais[animal] < 10:
                contador = fonte_contador.render(f'x0{pontos_animais[animal]}', True, BRANCO)
            else:
                contador = fonte_contador.render(f'x{pontos_animais[animal]}', True, BRANCO) 
            janela.blit(contador, (x_inicial + 27, altura_camera - 57))
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
                    cargas.append(Projectile(round(mago.x + mago.largura //2), round(mago.y + mago.altura//2), 4, facing_x, facing_y, poderes['poder1']))

    janela.blit(janela, (0,0)) #atualiza o timer e as barras corretamente

    pg.display.update()

# Encerra Pygame
pg.quit()
sys.exit()

