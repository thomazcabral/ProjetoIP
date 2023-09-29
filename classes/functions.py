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
def colisao(player, objeto, pontos_animais):
    if player.x + player.largura >= objeto.x >= player.x or objeto.x + objeto.largura >= player.x >= objeto.x:
        if player.y + player.altura >= objeto.y >= player.y or objeto.y + objeto.altura >= player.y >= objeto.y:
            objeto.morte()
            pontos_animais[objeto.nome] += 1

def colisao_dragao(player, objeto, vida_dragao):
    if player.x + player.largura >= objeto.x >= player.x or objeto.x + objeto.largura >= player.x >= objeto.x:
        if player.y + player.altura >= objeto.y >= player.y or objeto.y + objeto.altura >= player.y >= objeto.y:
            if vida_dragao < 1:
                objeto.morte()
                vida_dragao = 360
    return vida_dragao

def colisao_amigavel(objeto1, objeto2):
    if (objeto2.x + objeto2.largura >= objeto1.x >= objeto2.x or objeto1.x + objeto1.largura >= objeto2.x >= objeto1.x) and (objeto2.y + objeto2.altura >= objeto1.y >= objeto2.y or objeto1.y + objeto1.altura >= objeto2.y >= objeto1.y):
        return True

# Verifica se o dragão entra em contato com o mago e dá dano no mago
def dano_dragao(mago, dragao):
    if mago.x + mago.largura >= dragao.x >= mago.x or mago.x + mago.largura >= dragao.x + dragao.largura >= mago.x:
        if mago.y + mago.altura >= dragao.y >= mago.y or mago.y + mago.altura >= dragao.y + dragao.altura >= mago.y:
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
