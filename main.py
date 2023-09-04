import pygame #biblioteca usada pra criar e rodar o jogo
import sys #biblioteca usada para fechar o programa
import time #biblioteca usada para o timer funcionar

pygame.init() #Inicializa Pygame

# Configurações da janela
largura = 1880 
altura = 800 
janela = pygame.display.set_mode((largura, altura))

# Cores
branco = (255, 255, 255)
verde = (0, 255, 0)
# Posição inicial do retângulo
x = 100
y = 100

largura_retangulo = 50
altura_retangulo = 50

# Velocidade de movimento do retângulo
velocidade = 0.4
boost = 2000
fonte = pygame.font.Font(None, 36) # definindo as fontes
fonte_boost = pygame.font.Font(None, 36)
fonte_timer = pygame.font.Font(None, 36)

duracao_timer = 60 #em segundos
comeco_timer = time.time()

# Loop principal
running = True
while running:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed() # Obtém o estado das teclas
    # Move o retângulo
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
        if boost >= 0:
            boost -= 1
            velocidade = 0.7
    

    if not keys[pygame.K_LCTRL]: #define o estado do boost dele
        if boost < 2000:
            boost += 1
            situacao = "Recarregando..."
        else:
            situacao = "Carregado!"

    janela.fill(branco) # Preenche a janela com a cor de fundo

    pygame.draw.rect(janela, verde, (x, y, largura_retangulo, altura_retangulo)) # Desenha o retângulo

    texto_boost = fonte_boost.render(f'Boost: {boost}  {situacao}', True, (0, 0, 0)) #mostrando o boost
    janela.blit(texto_boost, (10, altura - 40)) #setando a localização do timer no canto inferior esquerdo

    tempo_atual = time.time() #começando o timer
    tempo_passado = tempo_atual - comeco_timer
    tempo_restante = max(duracao_timer - tempo_passado, 0) #faz com que não dê merda quando o tempo estoura
    minutos, segundos = divmod(int(tempo_restante), 60) #faz a divisão correta dos minutos e dos segundos no timer
    texto_timer = fonte_timer.render(f'Tempo: {minutos:02d}:{segundos:02d}', True, (0, 0, 0)) #mostrando o timer
    janela.blit(texto_timer, (largura - texto_timer.get_width() - 15, altura - 40)) #calculando a posição perfeita para o timer ficar no canto inferior direito da tela

    pygame.display.update() #atualiza a tela

# Encerra Pygame
pygame.quit()
sys.exit()
