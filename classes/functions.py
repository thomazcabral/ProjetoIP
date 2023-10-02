import pygame as pg

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
def colisao_poder(poder, animal, pontos_animais): #desacelerar e matar
    congelado = pg.mixer.Sound('assets/congelado.mp3')
    poof_sound = pg.mixer.Sound('assets/poof_sound.mp3')
    if colisao_amigavel(poder, animal):
            if poder.nome == 'poder1':
                pg.mixer.Sound.play(poof_sound)
                colisao(poder, animal, pontos_animais)
            elif poder.nome == 'poder2':
                pg.mixer.Sound.play(congelado)
                animal.congelado = 30

def colisao(mago, animal, pontos_animais):
    poof_sound = pg.mixer.Sound('assets/poof_sound.mp3')
    if colisao_amigavel(animal, mago):
                pg.mixer.Sound.play(poof_sound)
                animal.morte()
                pontos_animais[animal.nome] += 1

def colisao_dragao(player, objeto):
    if colisao_amigavel(objeto, player):
            objeto.vida -= 40
            if objeto.vida <= 0:
                objeto.morte()
                return True

def colisao_amigavel(objeto1, objeto2):
    if (objeto2.x + objeto2.largura >= objeto1.x >= objeto2.x or objeto1.x + objeto1.largura >= objeto2.x >= objeto1.x) and (objeto2.y + objeto2.altura >= objeto1.y >= objeto2.y or objeto1.y + objeto1.altura >= objeto2.y >= objeto1.y):
        return True

def colisao_coleta(mago, objeto):
    coleta = pg.mixer.Sound('assets/coletavel.mp3')
    if colisao_amigavel(mago, objeto):
        pg.mixer.Sound.play(coleta)
        if objeto.nome == 'vida':
            mago.vida += 100
            if mago.vida >= 1000:
                mago.vida = 1000
        elif objeto.nome == 'tempo':
            objeto.morte()
            return 20 #tempo a ser adicionado
        elif 'poder' in objeto.nome:
            mago.poder = objeto.nome 
        objeto.morte()
    return False

# Verifica se o dragão entra em contato com o mago e dá dano no mago
def dano_dragao(mago, dragao):
    if colisao_amigavel(dragao, mago):
            mago.vida -= 10
            if mago.vida <= 0:
                mago.vida = 0
            dragao.velocidade = 0

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

def draw_poder(cargas, janela, offset_x, offset_y):
    for poder in cargas:
        poder.draw(janela, offset_x, offset_y)

def draw_poder_hud(cargas, janela):
    for poder in cargas:
        poder.hud_draw(janela)
