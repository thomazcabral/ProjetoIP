import pygame
import sys

# Inicializa Pygame
pygame.init()

# Configurações da janela
largura = 1880
altura = 800
janela = pygame.display.set_mode((largura, altura))

# Cores
branco = (255, 255, 255)
verde = (0, 255, 0)
preto = (0, 0, 0)
# Posição inicial do retângulo
x = 100
y = 100

# Largura e altura do retângulo
largura_retangulo = 50
altura_retangulo = 50

# Velocidade de movimento do retângulo
velocidade = 0.4
timer = 2000
fonte = pygame.font.Font(None, 36)

# Loop principal
running = True
while running:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
    
    texto = fonte.render(f'{timer}', True, preto)
    recarregando = fonte.render('Recarregando...', True, preto)
    carregado = fonte.render('Carregado!', True, preto)
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
        if timer >= 0:
            timer -= 1
            velocidade = 0.7
            pygame.display.set_caption(f'{timer}')
    

    if not keys[pygame.K_LCTRL]:
        if timer < 2000:
            timer += 1
            pygame.display.set_caption(f'Recarregando... {timer}')
        else:
            pygame.display.set_caption('Carregado!')

    # Preenche a janela com a cor de fundo
    janela.fill(branco)

    # Desenha o retângulo
    pygame.draw.rect(janela, verde, (x, y, largura_retangulo, altura_retangulo))

    # Atualiza a tela
    pygame.display.update()

# Encerra Pygame
pygame.quit()
sys.exit()