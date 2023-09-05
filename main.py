import pygame
import sys

# Inicializa Pygame
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

# Posição inicial do retângulo
x = 100
y = 100

# Largura e altura do retângulo
largura_retangulo = 50
altura_retangulo = 50

# Velocidade de movimento do retângulo
velocidade = 0.4
stamina = 1000
fonte = pygame.font.Font(None, 24)

# Loop principal
running = True
while running:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
    
    janela.fill(branco)
    
    pygame.draw.rect(janela, verde, (x, y, largura_retangulo, altura_retangulo))
    
    ratio_stamina = stamina / 1000
    
    #Barra de vida    
    pygame.draw.rect(janela, vermelho, (10, 450, 200, 20))
    pygame.draw.rect(janela, verde, (10, 450, 200, 20))
    
    #Barra de stamina
    pygame.draw.rect(janela, branco, (10, 470, 200, 20))
    pygame.draw.rect(janela, amarelo, (10, 470, 200 * ratio_stamina, 20))
    pygame.display.flip()
    
    #Colisão com as bordas
    if x < 0:
        x = 0
    if x > largura - largura_retangulo:
        x = largura - largura_retangulo
    if y < 0:
        y = 0
    if y > altura - altura_retangulo:
        y = altura - altura_retangulo
    pygame.display.update()
    
    # Obtém o estado das teclas
    keys = pygame.key.get_pressed()
    # Move o retângulo para a direita quando a tecla da seta direita é pressionada
    if keys[pygame.K_RIGHT]:
        x += velocidade
    elif keys[pygame.K_LEFT]:
        x -= velocidade
    elif keys[pygame.K_UP]:
        y -= velocidade
    elif keys[pygame.K_DOWN]:
        y += velocidade
    if keys[pygame.K_LSHIFT]:
        velocidade = 0.2
    if not keys[pygame.K_LSHIFT]:
        velocidade = 0.4
    if keys[pygame.K_LCTRL]:
        if stamina >= 1:
            stamina -= 1
            velocidade = 0.7
    

    if not keys[pygame.K_LCTRL]:
        if stamina < 1000:
            stamina += 0.65

    # Atualiza a tela
    pygame.display.update()

# Encerra Pygame
pygame.quit()
sys.exit()
