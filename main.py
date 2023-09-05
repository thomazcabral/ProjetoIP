import pygame # biblioteca usada pra rodar o jogo
import sys # biblioteca usada pra fechar o programa
import time #biblioteca usada para o timer funcionar

class Retangulo:
    def __init__(self, x, y, largura, altura, velocidade, stamina):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.velocidade = velocidade
        self.stamina = stamina

    def move(self, keys):
        #método usado pra conferir qual tecla foi usada mais recentemente
        setas = {'RIGHT': 0, 'LEFT': 0, 'UP': 0, 'DOWN': 0} # Status de movimento inicial do retângulo (parado)
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
            self.velocidade = 0.2
        if not keys[pygame.K_LSHIFT]:
            self.velocidade = 0.4
        if keys[pygame.K_LCTRL]:
            if self.stamina >= 1:
                self.stamina -= 1
                self.velocidade = 0.7
        if not keys[pygame.K_LCTRL]:
            if self.stamina < 1000:
                self.stamina += 0.65

    def desenha(self, janela):
        pygame.draw.rect(janela, verde, (self.x, self.y, self.largura, self.altura))

pygame.init()

# Configurações da janela
largura = 1000
altura = 500
janela = pygame.display.set_mode((largura, altura))

# Cores
branco = (255, 255, 255)
verde = (0, 255, 0)
preto = (0, 0, 0)
amarelo = (255, 255, 0)
vermelho = (255, 0, 0)

# Cria o retângulo
retangulo = Retangulo(100, 100, 50, 50, 0.4, 1000) # x, y, largura, altura, velocidade e stamina

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
    pygame.draw.rect(janela, vermelho, (10, 450, 200, 20))
    pygame.draw.rect(janela, verde, (10, 450, 200, 20))

    # Barra de stamina
    pygame.draw.rect(janela, branco, (10, 470, 200, 20))
    pygame.draw.rect(janela, amarelo, (10, 470, 200 * ratio_stamina, 20))
    pygame.display.flip()

    # Colisão com as bordas
    if retangulo.x < 0:
        retangulo.x = 0
    if retangulo.x > largura - retangulo.largura:
        retangulo.x = largura - retangulo.largura
    if retangulo.y < 0:
        retangulo.y = 0
    if retangulo.y > altura - retangulo.altura:
        retangulo.y = altura - retangulo.altura
    pygame.display.update()

    retangulo.move(pygame.key.get_pressed())

    pygame.display.update()

# Encerra Pygame
pygame.quit()
sys.exit()
