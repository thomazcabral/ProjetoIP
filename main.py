import pygame
import sys
import time 
import random

class Inimigos:
    # Responsável por cada animal vivo
    inimigos_vivos =[]

    def __init__(self, velocidade):
        w = pygame.display.get_surface().get_width()
        h = pygame.display.get_surface().get_height()
        self.largura = w / (25.6 * 2)
        self.altura = h / (14.4 * 2)
        self.velocidade = velocidade
        self.raio = 100
        Inimigos.inimigos_vivos.append(self)

    def spawnar(self, retangulo):
        w = pygame.display.get_surface().get_width()	
        h = pygame.display.get_surface().get_height()	
        escolher = False
 	
        while not escolher:	
            valorx = random.randrange(0, w)	
            valory = random.randrange(0, h)
            # Só irão nascer animais em um raio maior que 300 px
            if ((retangulo.x + (retangulo.largura / 2) - valorx) ** 2 + (retangulo.y + (retangulo.altura / 2) - valory)** 2) ** (1/2) >= retangulo.raio:	
                self.x = valorx	
                self.y = valory	
                escolher = True
            for inimigo in Inimigos.inimigos_vivos:
                if inimigo != self and ((inimigo.x + (inimigo.largura / 2) - valorx) ** 2 + (inimigo.y + (inimigo.altura / 2) - valory)** 2) ** (1/2) < inimigo.raio:
                    escolher = False	

    def desenhar_inimigo(self, janela):
        pygame.draw.rect(janela, vermelho, (self.x, self.y, self.largura, self.altura))
        
    def morte(self):
        global contador
        contador += 1
        Inimigos.inimigos_vivos.remove(self)
    
    def move(self, retangulo, variacao_tempo):
        global velocidade_devagar
        global velocidade_rapida
        raio_alerta = retangulo.raio
        if retangulo.velocidade == velocidade_rapida:
            raio_alerta = raio_alerta * 1.5
        elif retangulo.velocidade == velocidade_devagar:
            raio_alerta = raio_alerta / 1.5
        distancia_x = retangulo.x - self.x
        distancia_y = retangulo.y - self.y
        antigo_x = self.x
        antigo_y = self.y
        if ((distancia_x)**2 + (distancia_y)**2)**(1/2) <= raio_alerta:
            if abs(distancia_x) > abs(distancia_y):
                if distancia_x < 0:
                    self.x += self.velocidade * variacao_tempo
                else:
                    self.x -= self.velocidade * variacao_tempo
            else:
                if distancia_y < 0:
                    self.y += self.velocidade * variacao_tempo
                else:
                    self.y -= self.velocidade * variacao_tempo
        for inimigo in Inimigos.inimigos_vivos:
                if inimigo != self and (abs(inimigo.x - self.x) < (inimigo.largura + self.largura) / 2 and abs(inimigo.y - self.y) < (inimigo.altura + self.altura) / 2):
                    self.x = antigo_x
                    self.y = antigo_y

class Retangulo:
    def __init__(self, x, y, velocidade, stamina):
        w = pygame.display.get_surface().get_width()
        h = pygame.display.get_surface().get_height()
        self.x = x
        self.y = y
        self.largura = w / 25.6
        self.altura = h / 14.4
        self.velocidade = velocidade
        self.stamina = stamina
        self.cansaco = 0
        self.img = pygame.image.load('mago_down.png')
        self.raio = 300

    def move(self, keys, variacao_tempo):
        global janela
        #método usado pra conferir qual tecla foi usada mais recentemente
        global setas
        global stamina_padrao
        global tela_cheia
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            setas['RIGHT'] += 1
        else:
            setas['RIGHT'] = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            setas['LEFT'] += 1
        else:
            setas['LEFT'] = 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            setas['UP'] += 1
        else:
            setas['UP'] = 0
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
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
        
        if keys[pygame.K_F11] and not tela_cheia:
            janela = pygame.display.set_mode((largura, altura), pygame.FULLSCREEN)
            tela_cheia = True
        if keys[pygame.K_ESCAPE] and tela_cheia:
            janela = pygame.display.set_mode((largura, altura))
            tela_cheia = False

        if escolhida:
            if escolhida == 'RIGHT':
                self.img = pygame.image.load('mago_right.png')
                self.x += self.velocidade * variacao_tempo
            elif escolhida == 'LEFT':
                self.img = pygame.image.load('mago_left.png')
                self.x -= self.velocidade * variacao_tempo
            elif escolhida == 'UP':
                self.img = pygame.image.load('mago_up.png')
                self.y -= self.velocidade * variacao_tempo
            elif escolhida == 'DOWN':
                self.img = pygame.image.load('mago_down.png')
                self.y += self.velocidade * variacao_tempo
            else:
                self.img = pygame.image.load('mago_down.png')
            
        if keys[pygame.K_LSHIFT]:
            self.velocidade = 0.05
        if not keys[pygame.K_LSHIFT]:
            self.velocidade = 0.1
        if keys[pygame.K_LCTRL] and escolhida:
            if self.stamina >= 1 and self.cansaco == 0:
                self.stamina -= 5
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
        imagem = pygame.image.load('mago_down.png')
        w, h = imagem.get_size()
        self.largura = w * escala
        self.altura = h * escala
        redimensionar = pygame.transform.smoothscale(self.img, ((w*escala), (h*escala)))
        janela.blit(redimensionar, (self.x, self.y))


pygame.init()

# Configurações da janela
largura = 1280
altura = 720
janela = pygame.display.set_mode((largura, altura))
tela_cheia = False

# Cores
branco = (255, 255, 255)
verde = (0, 255, 0)
preto = (0, 0, 0)
amarelo = (255, 255, 0)
vermelho = (255, 0, 0)

fonte_timer_e_contador = pygame.font.Font(None, 36)
duracao_timer = 60 #em segundos
comeco_timer = time.time() #início do timer
clock = pygame.time.Clock()

velocidade_devagar = 0.05
velocidade_padrao = 0.1
velocidade_rapida = 0.15

stamina_padrao = 500

ponto_inicial = (100, 100)
# Cria o retângulo
retangulo = Retangulo(ponto_inicial[0], ponto_inicial[1], velocidade_padrao, stamina_padrao) # x, y, largura, altura, velocidade e stamina

# Spawnar os animais, foi escolhido 3 mas pode ser arbitrário
inimigos_vivos = []
contador = 0
for i in range(3):
  locals()['inimigo' + str(i)] = Inimigos(velocidade_devagar)
  locals()['inimigo' + str(i)].spawnar(retangulo)

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
    if variavel.y > height - variavel.altura:
        variavel.y = height - variavel.altura
    return variavel

# Colisão do player com os animais
def colisao(player, objeto):
    if player.x + player.largura >= objeto.x >= player.x or player.x + player.largura >= objeto.x + objeto.largura >= player.x:
        if player.y + player.altura >= objeto.y >= player.y or player.y + player.altura >= objeto.y + objeto.altura >= player.y:
            objeto.morte()

setas = {'RIGHT': 0, 'LEFT': 0, 'UP': 0, 'DOWN': 0} # Status de movimento inicial do retângulo (parado)
# Loop principal
running = True


while running:
    
    # A movimentação é em função do tempo, se rodar muito ciclos ele para e volta dps
    variacao_tempo = clock.tick(30)

    width = pygame.display.get_surface().get_width()
    height = pygame.display.get_surface().get_height()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
    
    exibir_janela = janela.copy() #copia a janela e evita com que algo fique "piscando" na tela devido a atualizações constantes

    exibir_janela.fill(branco)

    retangulo.desenhar_mago(exibir_janela)
    
    # há uma pequena chance de surgir um animal cada vez que o loop roda
    chance = random.randrange(1,500)
    if chance == 1 and len(Inimigos.inimigos_vivos) <= 20:
        locals()['inimigo' + str(i)] = Inimigos(velocidade_devagar)
        locals()['inimigo' + str(i)].spawnar(retangulo)
    for inimigo in Inimigos.inimigos_vivos:
        inimigo.desenhar_inimigo(exibir_janela)
        


    ratio_stamina = retangulo.stamina / 1000

    # Barra de vida
    width = pygame.display.get_surface().get_width()
    height = pygame.display.get_surface().get_height()
    pygame.draw.rect(exibir_janela, vermelho, (width / (largura/10), height / (altura/(altura-50)), width / (largura/200), height / (altura/20)))
    pygame.draw.rect(exibir_janela, verde, (width / (largura/10), height / (altura/(altura-50)), width / (largura/200), height / (altura/20)))

    # Barra de stamina
    pygame.draw.rect(exibir_janela, branco, (width / (largura/10), height / (altura/(altura-30)), width / (largura/200), height / (altura/20)))
    pygame.draw.rect(exibir_janela, amarelo, (width / (largura/10), height / (altura/(altura-30)), width * ratio_stamina / (largura/200), height / (altura/20)))
    pygame.display.flip()

    #movimentação dos inimigos
    for inimigo in Inimigos.inimigos_vivos:
        inimigo.move(retangulo, variacao_tempo)
    # Colisão com as bordas
    retangulo = borda(retangulo)
    for inimigo in Inimigos.inimigos_vivos: 
        inimigo = borda(inimigo)
        inimigo = colisao(retangulo, inimigo)


         
    pygame.display.update()

    retangulo.move(pygame.key.get_pressed(), variacao_tempo)

    tempo_atual = time.time()
    tempo_passado = tempo_atual - comeco_timer
    tempo_restante = max(0, duracao_timer - tempo_passado) #evite com que o timer dê errado quando acabe
    minutos, segundos = divmod(int(tempo_restante), 60) #faz a divisão correta entre minutos e segundos
    texto_timer = fonte_timer_e_contador.render(f'Tempo: {minutos:02d}:{segundos:02d}', True, (0, 0, 0)) #texto, situação de aparecimento, cor
    exibir_janela.blit(texto_timer, (largura - texto_timer.get_width() - 15, altura - 40))

    texto_contador = fonte_timer_e_contador.render(f'Pontuação: {contador}', True, (0, 0, 0))
    exibir_janela.blit(texto_contador, (largura - texto_timer.get_width() - 200, altura - 40))

    janela.blit(exibir_janela, (0,0)) #atualiza o timer e as barras corretamente

    pygame.display.update()

# Encerra Pygame
pygame.quit()
sys.exit()
