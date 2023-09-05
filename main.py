import pygame # biblioteca usada pra rodar o jogo
import sys # biblioteca usada pra fechar o programa
import time #biblioteca usada para o timer funcionar

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
        if keys[pygame.K_RIGHT]:
            setas['RIGHT'] += 1
        else:
            setas['RIGHT'] = 0
        if keys[pygame.K_LEFT]:
            setas['LEFT'] += 1
        else:
            setas['LEFT'] = 0
        if keys[pygame.K_UP]:
            setas['UP'] += 1
        else:
            setas['UP'] = 0
        if keys[pygame.K_DOWN]:
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
        if keys[pygame.K_LCTRL]:
            if self.stamina >= 1:
                self.stamina -= 1
                self.velocidade = 1.1
        if not keys[pygame.K_LCTRL]:
            if self.stamina < 1000:
                self.stamina += 0.65

    def desenha(self, janela):
        w = pygame.display.get_surface().get_width()
        h = pygame.display.get_surface().get_height()
        self.largura = w / 25.6
        self.altura = h / 14.4
        pygame.draw.rect(janela, verde, (self.x, self.y, self.largura, self.altura))

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

# Cria o retângulo
retangulo = Retangulo(100, 100, 0.7, 1000) # x, y, largura, altura, velocidade e stamina

setas = {'RIGHT': 0, 'LEFT': 0, 'UP': 0, 'DOWN': 0} # Status de movimento inicial do retângulo (parado)
# Loop principal
running = True
while running:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
    
    janela.fill(branco)

    retangulo.desenha(janela)

    ratio_stamina = retangulo.stamina / 1000

    # Barra de vida
    width = pygame.display.get_surface().get_width()
    height = pygame.display.get_surface().get_height()
    pygame.draw.rect(janela, vermelho, (width / (1280/10), height / (720/670), width / (1280/200), height / (720/20)))
    pygame.draw.rect(janela, verde, (width / (1280/10), height / (720/670), width / (1280/200), height / (720/20)))

    # Barra de stamina
    pygame.draw.rect(janela, branco, (width / (1280/10), height / (720/690), width / (1280/200), height / (720/20)))
    pygame.draw.rect(janela, amarelo, (width / (1280/10), height / (720/690), width * ratio_stamina / (1280/200), height / (720/20)))
    pygame.display.flip()

    # Colisão com as bordas
    if retangulo.x < 0:
        retangulo.x = 0
    if retangulo.x > width - retangulo.largura:
        retangulo.x = width - retangulo.largura
    if retangulo.y < 0:
        retangulo.y = 0
    if retangulo.y > height - retangulo.altura:
        retangulo.y = height - retangulo.altura
    pygame.display.update()

    retangulo.move(pygame.key.get_pressed())

    pygame.display.update()

# Encerra Pygame
pygame.quit()
sys.exit()
