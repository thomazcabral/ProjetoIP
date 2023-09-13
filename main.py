import pygame as pg
import sys
import time
import random

class Inimigos(pg.sprite.Sprite):
    # Responsável por cada animal vivo
    inimigos_vivos = []

    def __init__(self, infos, nome):
        super().__init__()
        w = pg.display.get_surface().get_width()
        h = pg.display.get_surface().get_height()
        self.largura = w / (25.6 * 2)
        self.altura = h / (14.4 * 2)
        self.nome = nome
        self.velocidade_padrao = infos[self.nome]['velocidade']
        self.velocidade = self.velocidade_padrao
        self.cor = infos[self.nome]['referencia']
        self.raio = 100
        self.direcao = False
        self.mov_idle = 0
        self.velocidade_idle = 0.03
        self.repouso = 0
        Inimigos.inimigos_vivos.append(self)

    def spawnar(self, retangulo):
        w = pg.display.get_surface().get_width()	
        h = pg.display.get_surface().get_height()	
        escolher = False
        global Parede
        while not escolher:	
            valorx = random.randrange(0, w)	
            valory = random.randrange(0, h - 60)
            # Só irão nascer animais em um raio maior que 300 px
            if ((retangulo.x + (retangulo.largura / 2) - valorx) ** 2 + (retangulo.y + (retangulo.altura / 2) - valory)** 2) ** (1/2) >= retangulo.raio:	
                self.x = valorx	
                self.y = valory	
                escolher = True
                for inimigo in Inimigos.inimigos_vivos:
                    if inimigo != self and ((inimigo.x + (inimigo.largura / 2) - valorx) ** 2 + (inimigo.y + (inimigo.altura / 2) - valory)** 2) ** (1/2) < inimigo.raio:
                        escolher = False	
                for parede in Parede.paredes:
                    if colisao_amigavel(self, parede):
                        escolher = False

    def desenhar_inimigo(self, janela):
        pg.draw.rect(janela, self.cor, (self.x, self.y, self.largura, self.altura))
        pg.draw.rect(janela, self.cor, (self.x, self.y, self.largura, self.altura))
        
    def morte(self):
    
        Inimigos.inimigos_vivos.remove(self)
    
    def move(self, retangulo, variacao_tempo):
        global velocidade_devagar
        global velocidade_rapida
        global Parede
        raio_alerta = retangulo.raio
        if retangulo.velocidade == velocidade_rapida:
            raio_alerta = raio_alerta * 1.5
        elif retangulo.velocidade == velocidade_devagar:
            raio_alerta = raio_alerta / 1.5
        distancia_x = retangulo.x - self.x
        distancia_y = retangulo.y - self.y
        antigo_x = self.x
        antigo_y = self.y
        direcoes = ['direita', 'esquerda', 'baixo', 'cima']
        if not self.direcao and self.repouso == 0:
            self.direcao = random.choice(direcoes)
            self.repouso = random.randrange(160, 240)
            self.mov_idle = random.randrange(120,150)
            self.velocidade = self.velocidade_idle
        if self.mov_idle == 0:
            self.direcao = False
            self.velocidade = self.velocidade_padrao
        else: 
            self.mov_idle -= 1
        if self.repouso > 0:
            self.repouso -= 1

        if ((distancia_x)**2 + (distancia_y)**2)**(1/2) <= raio_alerta:
            self.mov_idle = 0
            if abs(distancia_x) > abs(distancia_y):
                self.velocidade = self.velocidade_padrao
                if distancia_x < 0:
                    self.direcao = 'direita'
                else:
                    self.direcao = 'esquerda'
            else:
                if distancia_y < 0:
                    self.direcao = 'baixo'
                else:
                    self.direcao = 'cima'

        if self.direcao == 'direita':
            self.x += self.velocidade * variacao_tempo
        elif self.direcao == 'esquerda':
            self.x -= self.velocidade * variacao_tempo
        elif self.direcao == 'baixo':
            self.y += self.velocidade * variacao_tempo
        elif self.direcao == 'cima':
            self.y -= self.velocidade * variacao_tempo
        bloqueio = []
        for k in Inimigos.inimigos_vivos:
            if k != self:
                bloqueio.append(k)
        for k in Parede.paredes:
            bloqueio.append(k)
        for inimigo in bloqueio:
            if colisao_amigavel(self, inimigo):
                self.x = antigo_x
                self.y = antigo_y

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

    def move(self, keys, variacao_tempo):
        global janela
        #método usado pra conferir qual tecla foi usada mais recentemente
        global setas
        global stamina_padrao
        global tela_cheia
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
        
        if keys[pg.K_F11] and not tela_cheia:
            janela = pg.display.set_mode((LARGURA, ALTURA), pg.FULLSCREEN)
            tela_cheia = True
        if keys[pg.K_ESCAPE] and tela_cheia:
            janela = pg.display.set_mode((LARGURA, ALTURA))
            tela_cheia = False
        
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
            if colisao_amigavel(self, parede,):
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


class Parede:
    paredes = []
    raio = 200
    def __init__(self, proporcao):
        w = pg.display.get_surface().get_width()
        h = pg.display.get_surface().get_height()
        self.largura = ((w + h) / 2) * proporcao
        self.altura = self.largura / 2
        self.raio = Parede.raio 
        escolher = False
        global retangulo
        while not escolher:
            self.x = random.randrange(0, int(w - self.largura))
            self.y = random.randrange(50, int(h - 60 - self.altura))
            if not colisao_amigavel(self, retangulo):
                escolher = True
            for parede in Parede.paredes:
                if ((parede.x + (parede.largura / 2) - self.x) ** 2 + (parede.y + (parede.altura / 2) - self.y)** 2) ** (1/2) < parede.raio:
                    escolher = False

        Parede.paredes.append(self)
    #arbitrei mais q tudo pra fazer isso aq, nn faço ideia de como o calculo deveria ser
    def desenhar_tronco(self):
        self.img = pg.image.load('tronco.png')
        x = self.img.get_size()[0]
        y = self.img.get_size()[1]
        escala = self.largura * 2/ x
        redimensionar = pg.transform.smoothscale(self.img, ((x*escala), (y*escala)))
        janela.blit(redimensionar, (self.x - (self.largura / 2), self.y))

    def desenhar_folhas(self):
        self.img = pg.image.load('folhas.png')
        self.img.set_alpha(210)
        x = self.img.get_size()[0]
        y = self.img.get_size()[1]
        escala = self.largura * 3/ x
        redimensionar = pg.transform.smoothscale(self.img, ((x*escala), (y*escala)))
        janela.blit(redimensionar, (self.x - (self.largura), self.y - 5 * self.altura))

 


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
# Cria o retângulo
retangulo = Retangulo(ponto_inicial[0], ponto_inicial[1], velocidade_padrao, stamina_padrao) # x, y, largura, altura, velocidade e stamina

#cria as paredes
num_arvores = random.randrange(4,8)
for j in range(num_arvores):
   locals()['parede' + str(j)] = Parede(0.05)

# Spawnar os animais, foi escolhido 3 mas é arbitrário

# Spawnar os animais, foi escolhido 3, mas pode ser arbitrário

pontos_inimigos = {}
for animal in infos.keys():
    pontos_inimigos[animal] = 0
for i in range(3):
    nome = random.choice([k for k in infos.keys()])
    locals()['inimigo' + str(i)] = Inimigos(infos, nome)
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

    for x in range(0, width, 50):
        for y in range(0, height, 50):
            janela.blit(tilemap[mapa[(x, y)]], (x, y))


    
    for j in range(num_arvores):
        locals()['parede' + str(j)].desenhar_tronco()

    retangulo.desenhar_mago(janela)
    
    # há uma pequena chance de surgir um animal cada vez que o loop roda

    chance = random.randrange(1,500)
    total_vivos = len(Inimigos.inimigos_vivos)
    if total_vivos == 0 or (chance == 1 and total_vivos <= 20):
        nome = random.choice([j for j in infos.keys()])
        locals()['inimigo' + str(i)] = Inimigos(infos, nome)
        locals()['inimigo' + str(i)].spawnar(retangulo)
    for inimigo in Inimigos.inimigos_vivos:
        inimigo.desenhar_inimigo(janela)
    
    for j in range(num_arvores):
        locals()['parede' + str(j)].desenhar_folhas()
    ratio_stamina = retangulo.stamina / 1000
    
    #lugar de informacões:
    width = pg.display.get_surface().get_width()
    height = pg.display.get_surface().get_height()
    janela.blit(hud, (-200, height - 60))

    #Moldura barra de vida
    largura_barra = 200
    altura_barra = 15
    raio_borda = 4
    espessura = 2
    
    #Fundo barra de stamina
    pg.draw.rect(janela, CINZA, (width / (LARGURA/10), height / (ALTURA/(ALTURA-28)), largura_barra, altura_barra), border_radius=raio_borda)

    #Fundo barra de vida
    pg.draw.rect(janela, CINZA, (width / (LARGURA/10), height / (ALTURA/(ALTURA-44)), largura_barra, altura_barra), border_radius=raio_borda)

    # Barra de vida
    pg.draw.rect(janela, VERDE, (width / (LARGURA/10), height / (ALTURA/(ALTURA-44)), largura_barra, altura_barra), border_radius=raio_borda)
    pg.draw.rect(janela, MARROM_ESCURO, (width / (LARGURA/10), height / (ALTURA/(ALTURA-44)), largura_barra, altura_barra), espessura, border_radius=raio_borda)

    # Barra de stamina
    pg.draw.rect(janela, AMARELO, (width / (LARGURA/10), height / (ALTURA/(ALTURA-28)), largura_barra * ratio_stamina, altura_barra), border_radius=raio_borda)
    pg.draw.rect(janela, MARROM_ESCURO, (width / (LARGURA/10), height / (ALTURA/(ALTURA-28)), largura_barra, altura_barra), espessura, border_radius=raio_borda)


    #movimentação dos inimigos
    for inimigo in Inimigos.inimigos_vivos:
        inimigo.move(retangulo, variacao_tempo)
    # Colisão com as bordas
    retangulo = borda(retangulo)
    for inimigo in Inimigos.inimigos_vivos: 
        inimigo = borda(inimigo)
        inimigo = colisao(retangulo, inimigo)

    retangulo.move(pg.key.get_pressed(), variacao_tempo)

    tempo_atual = time.time()
    tempo_passado = tempo_atual - comeco_timer
    tempo_restante = max(0, duracao_timer - tempo_passado) #evite com que o timer dê errado quando acabe
    minutos, segundos = divmod(int(tempo_restante), 60) #faz a divisão correta entre minutos e segundos
    texto_timer = fonte.render(f'Tempo: {minutos:02d}:{segundos:02d}', True, (0, 0, 0)) #texto, situação de aparecimento, cor
    janela.blit(texto_timer, (LARGURA - texto_timer.get_width() - 15, ALTURA - 50))
    x_inicial = LARGURA - texto_timer.get_width() - 200 
    for animal in reversed(pontos_inimigos.keys()):
        texto_contador = fonte.render(f'{animal}: {pontos_inimigos[animal]}', True, (0, 0, 0))
        janela.blit(texto_contador, (x_inicial, ALTURA - 50))
        x_inicial -= 150

    janela.blit(janela, (0,0)) #atualiza o timer e as barras corretamente

    pg.display.update()

# Encerra Pygame
pg.quit()
sys.exit()
