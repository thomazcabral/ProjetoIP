import pygame # biblioteca usada pra rodar o jogo
import sys # biblioteca usada pra fechar o programa
import time #biblioteca usada para o timer funcionar
import random #biblioteca usada para randomizar números

class Inimigos:
    # Responsável por cada animal vivo
    inimigos_vivos =[]

    def __init__(self, velocidade):
        w = pygame.display.get_surface().get_width()
        h = pygame.display.get_surface().get_height()
        self.largura = w / (25.6 * 2)
        self.altura = h / (14.4 * 2)
        self.velocidade = velocidade
        Inimigos.inimigos_vivos.append(self)

    def spawnar(self, retangulo):
        w = pygame.display.get_surface().get_width()	
        h = pygame.display.get_surface().get_height()	
        escolher = False	
        while not escolher:	
            valorx = random.randrange(0, w)	
            valory = random.randrange(0, h)	
            # Só irão nascer animais em um raio maior que 300 px
            if (abs(retangulo.x - valorx) ** 2 + abs(retangulo.y - valory)** 2) ** (1/2) >= 300:	
                self.x = valorx	
                self.y = valory	
                escolher = True

    def desenhar_inimigo(self, janela):
        pygame.draw.rect(janela, vermelho, (self.x, self.y, self.largura, self.altura))
        
    def morte(self):
        global contador
        contador += 1
        Inimigos.inimigos_vivos.remove(self)
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

    def move(self, keys):
        global janela
        #método usado pra conferir qual tecla foi usada mais recentemente
        global setas
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
        print(setas)
        
        if keys[pygame.K_F11]:
            janela = pygame.display.set_mode((largura, altura), pygame.FULLSCREEN)
        if keys[pygame.K_ESCAPE]:
            janela = pygame.display.set_mode((largura, altura))

        if escolhida:
            if escolhida == 'RIGHT':
                self.x += self.velocidade
            elif escolhida == 'LEFT':
                self.x -= self.velocidade
            elif escolhida == 'UP':
                self.y -= self.velocidade
            elif escolhida == 'DOWN':
                self.y += self.velocidade

            
        if keys[pygame.K_LSHIFT]:
            self.velocidade = 0.4
        if not keys[pygame.K_LSHIFT]:
            self.velocidade = 0.7
        if keys[pygame.K_LCTRL] and escolhida:
            if self.stamina >= 1:
                self.stamina -= 1
                self.velocidade = 1.1
        else:
            if self.stamina < 1000:
                self.stamina += 0.65

    def desenhar_mago(self, janela):
        global width
        global height
        self.largura = width / 25.6
        self.altura = height / 14.4
        pygame.draw.rect(janela, verde, (self.x, self.y, self.largura, self.altura)) #tá errado


pygame.init()

# Configurações da janela
largura = 1280
altura = 720
janela = pygame.display.set_mode((largura, altura))

# Cores
branco = (255, 255, 255)
verde = (0, 255, 0)
preto = (0, 0, 0)
amarelo = (255, 255, 0)
vermelho = (255, 0, 0)

fonte_timer_e_contador = pygame.font.Font(None, 36)
duracao_timer = 60 #em segundos
comeco_timer = time.time() #início do timer

# Cria o retângulo
retangulo = Retangulo(100, 100, 0.7, 1000) # x, y, largura, altura, velocidade e stamina

# Spawnar os animais, foi escolhido 3 mas pode ser arbitrário
inimigos_vivos = []
contador = 0
for i in range(3):
  locals()['inimigo' + str(i)] = Inimigos(0.5)
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
    
    print(contador)
    width = pygame.display.get_surface().get_width()
    height = pygame.display.get_surface().get_height()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
    
    exibir_janela = janela.copy() #copia a janela e evita com que algo fique "piscando" na tela devido a atualizações constantes

    exibir_janela.fill(branco)

    retangulo.desenhar_mago(exibir_janela)
    
    # há uma pequena chance de surgir um animal cada vez que o loop roda
    chance = random.randrange(1,300)
    if chance == 1:
        locals()['inimigo' + str(i)] = Inimigos(0.5)
        locals()['inimigo' + str(i)].spawnar(retangulo)
        inimigos_vivos.append(i)
    for inimigo in Inimigos.inimigos_vivos:
        inimigo.desenhar_inimigo(exibir_janela)


    ratio_stamina = retangulo.stamina / 1000

    # Barra de vida
    width = pygame.display.get_surface().get_width()
    height = pygame.display.get_surface().get_height()
    pygame.draw.rect(exibir_janela, vermelho, (width / (1280/10), height / (720/670), width / (1280/200), height / (720/20)))
    pygame.draw.rect(exibir_janela, verde, (width / (1280/10), height / (720/670), width / (1280/200), height / (720/20)))

    # Barra de stamina
    pygame.draw.rect(exibir_janela, branco, (width / (1280/10), height / (720/690), width / (1280/200), height / (720/20)))
    pygame.draw.rect(exibir_janela, amarelo, (width / (1280/10), height / (720/690), width * ratio_stamina / (1280/200), height / (720/20)))
    pygame.display.flip()

    # Colisão com as bordas
    retangulo = borda(retangulo)
    for inimigo in Inimigos.inimigos_vivos: 
        inimigo = borda(inimigo)
        inimigo = colisao(retangulo, inimigo)

         
    pygame.display.update()

    retangulo.move(pygame.key.get_pressed())

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
