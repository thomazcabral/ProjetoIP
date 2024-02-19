
# The Forest Mage

Projeto que consiste em um jogo 2d criado por meio da linguagem Python e da biblioteca Pygame. Disciplina de Introdução à Programação (IP), ofertada no Centro de Informática (CIn) da Universidade Federal de Pernambuco (UFPE).

This project description is also available in english in the "README_english.md" file in this repository.


## Funcionamento do jogo

- Instalação da versão mais atualizada de Python;
- Instalação da biblioteca Pygame por meio do comando pip install pygame;
- Instalação da bilbioteca numpy por meio do comando pip install numpy.
## Participantes

- [Diana Rocha Silva](https://github.com/Diana-RS)
- [Filip Pawlowski Augusto Fernandes](https://github.com/filip-fernandes)
- [João Luís da Silva Marrocos](https://github.com/jlsm2)
- [Pedro Henrique Moraes de Sousa Silva](https://github.com/pedroagaeme)
- [Thomaz Cabral Corrêa de Araújo](https://github.com/thomazcabral)

## Ideação e objetivos

A ideia principal da equipe foi de criar um jogo com perspectiva top-down, ou seja, um tipo de jogo onde a câmera e a perspectiva permitem ao jogador observar o ambiente e os personagens de uma visão aérea, geralmente de cima para baixo. Outra ideia nossa era de criar um jogo de coleta, em que um personagem principal se moveria em direção a outros objetos que tentariam manter-se distantes do personagem principal. Para a criação do jogo visualmente, demoramos um tempo para termos uma ideia boa e aplicável, até nos inspirarmos no jogo “Stardew Valley”, uma simulação de um personagem realizando ações em um ambiente bucólico. Apesar disso, os recursos visuais do jogo foram alterados gradativamente até a identidade visual diferenciar-se demasiadamente desse outro jogo.

Em geral, o jogo é composto por um mago que tem como objetivo escapar do dragão, o qual pode ser eliminado posteriormente, e coletar a maior quantidade possível de animais no período determinado de tempo. O mago consegue coletar os animais encostando neles ou por meio dos poderes, os quais são habilidades especiais do mago que aparecem no mapa. Entre tais poderes, temos a coleta instantânea dos animais, desaceleração temporária dos animais, aumento da quantidade de tempo disponível e a elevação da vida do mago. O mapa é composto por tiles (quadrados) gerados aleatoriamente, ou seja, a cada vez que alguém joga, o mapa gerado é diferente. Ele também é decorado com árvores, folhas, flores, frutas, cogumelos e um rio. Na parte inferior do jogo, há um menu de informações acerca do jogo atual, relatando a vida e a estamina do mago, o poder que o mago coletou e que está pronto para ser utilizado, além do contador de quantos animais foram coletados. É de suma importância ressaltar a existência de um menu inicial, o qual possibilita o jogador iniciar o jogo ou sair dele, e um final, o qual exibe a pontuação do jogador, exibe a possibilidade dele também sair do jogo ou iniciar outro. Caso o jogador perca a sua vida devido ao dano recebido pelo dragão, ele é declarado derrotado. Caso contrário, sua pontuação aparecerá na tela.
## Arquitetura do projeto

O código inteiro foi dividido nas seguintes partes com o intuito de deixá-lo mais intuitivo e inteligível: 

- **Assets**: Pasta onde se encontram todas as imagens que são exibidas no jogo, incluindo os animais e seus respectivos sprites, o fundo do menu, detalhes que são mostrados no mapa do jogo, como cogumelos, flores, folhas e frutas, projetéis lançados tanto pelo mago quanto pelo dragão, madeira que constitui o menu onde aparecem informações úteis do jogo, poderes que aparecem no mapa, os tiles do mapa, da ponte e do rio, além das árvores e das fontes que são utilizadas no programa.
- **Classes**: Pasta em que os objetos e suas ações presentes no jogo se localizam, em um ambiente totalmente programado em orientação a objetos (POO). Entre as funções que se encontram neste local, temos: a movimentação e o aparecimento aleatório dos animais e do mago e a criação de todos os objetos na tela.
- **Functions**: Arquivo em que todas as funções que são utilizadas no código principal estão definidas: a colisão do mago com a borda, do mago com os animais, do mago com os poderes e dos objetos com as paredes, impedindo que eles sigam o movimento natural, além de uma função que envolve a criação do rio.
- **Config**: Arquivo em que as constantes são definidas, como cores, configurações de tamanho de tela, quantidade dos animais, velocidade dos animais e do mago, além de configurações gerais do mapa.
- **Engine**: Principal partição do código, a qual faz com que o jogo entre em um loop e funcione corretamente. É importante ressaltar que esta parte que está contida na classe “Engine” é completamente trabalhada em POO. É nesse segmento que os objetos são criados, renderizados, em que o temporizador é criado e que a quantidade de animais coletados e contabilizada.
- **Main**: Pequeno trecho de código, o qual garante que um bloco específico de código seja executado apenas quando o script Python é executado diretamente como o programa principal e não quando é importado como um módulo em outro script.
## Bibliotecas e ferramentas

- **Pygame**: biblioteca utilizada com o intuito de utilizar suas ferramentas para o jogo ser criado e funcionar. Utilizamos suas funções variadas como funções para desenhar na tela, criar janelas, estabelecer a fonte de um determinado texto, implementar imagens no jogo, além de encerrar o programa.
- **Sys**: biblioteca usada apenas para encerrar o programa.
- **Time**: biblioteca utilizada com o objetivo de criar e exibir na tela um temporizador, que exibe ao usuário quanto tempo de jogo ele possui até o jogo encerrar.
- **Random**: Como o mapa do jogo é gerado aleatoriamente, ou seja, toda vez que alguém for jogar, a dinâmica e o visual do jogo será completamente diferente, essa biblioteca foi bastante utilizada para essa função, escolhendo números e imagens aleatórias para melhorar a jogabilidade do programa, além de escolher a direção quando os animais não estão próximos do mago. A parte em que ela foi mais utilizada foi na geração aleatória dos rios, na geração das árvores e na posição dos animais.
## Divisão do trabalho

- Diana: criação de pixel arts, elaboração do menu inicial e final, modularização do código
- Filip: reestruturação do código, criação de certas funções nas classes
- João: criação dos projéteis, das animações e do menu de informações do jogo, ornamentação do dragão
- Pedro: Ideação do projeto, criação dos animais, do rio e da aleatoriedade dos mapas, implementação das artes
- Thomaz: criação do dragão, implementação de POO, elaboração do relatório e da apresentação

É bom citar que todos conseguiram praticar o que foi aprendido na disciplina durante o semestre e que este projeto foi todo realizado em conjunto, com todos compreendendo o que foi feito de acordo com o devido planejamento.
## Conceitos na prática

- **Condicionais**: O trecho do código em que os comandos condicionais mais foram utilizados localizam-se na checagem da colisão dos personagens entre si e entre eles e as paredes existentes, que consistem na borda da janela em que o jogo funciona, as árvores e o rio. Mais especificamente, utilizamos condicionais devido à necessidade de comparação entre a posição (x e y) dos objetos para, posteriormente, o objeto não conseguir mais se locomover mesmo que ele tente ou ele desapareça, no caso da colisão do mago com os animais os quais ele caça. Além disso, eles também foram usados para verificar a última tecla apertada pelo usuário a fim de que o poder não seja arremessado para a direção errada e para evitar possíveis problemas na movimentação do mago. Para a atualização das barras de vida e de estamina, sua diminuição quando o personagem recebe dano e gasta sua energia, respectivamente, também foram utilizadas proposições condicionais. Exemplo de uso de condicionais para o funcionamento correto da câmera:

```py
def align_camera(self, largura_camera, altura_camera) -> None:
        self.offset_x = self.mago.x - (largura_camera / 2)
        if self.offset_x < 0:
            self.offset_x = 0
        elif self.offset_x + (largura_camera) > self.screen_config["LARGURA_MAPA"]:
            self.offset_x = self.screen_config["LARGURA_MAPA"] - largura_camera
            self.offset_y = self.mago.y - (altura_camera / 2)
        if self.offset_y < 0:
            self.offset_y = 0
        elif self.offset_y + (altura_camera) > self.screen_config["ALTURA_MAPA"]:
            self.offset_y = self.screen_config["ALTURA_MAPA"] - altura_camera
```

- **Laços de repetição**: Eles foram demasiadamente utilizados para a checagem da colisão entre todos os objetos existentes no programa e também foram úteis para iterar sobre cada animal e chamar a função que os movimenta, fazendo com que fossem criados bloqueios para o mago conseguir nascer longe dos animais e dos poderes e não conseguir nascer em árvores nem no rio. O loop principal do programa e a geração aleatória de rios também funciona devido aos laços de repetição. Exemplo do uso dessa ferramenta para iterar sobre listas de objetos para aplicar colisão:

```py
	 		#checando colisão com animais
            for animal in Animais.animais_vivos:
                if functions.colisao_amigavel(poder, animal):
                    functions.colisao_poder(poder, animal, self.pontos_animais)
                    self.cargas.pop(self.cargas.index(poder))

            #checando colisão com o dragao
            for dragao in Dragao.dragoes_vivos:
                if functions.colisao_amigavel(poder, dragao):
                    functions.colisao_dragao(poder, dragao)
                    self.cargas.pop(self.cargas.index(poder))

            #checando colisão com paredes        
            for parede in Parede.paredes:
                if functions.colisao_amigavel(poder, parede):
                    self.cargas.pop(self.cargas.index(poder))
```
- **Listas**: As listas foram usadas para armazenar os animais vivos e os já coletados, os projéteis que estão aparecendo no mapa, cada tilemap existente, o rio do jogo atual, os poderes dispostos no mapa. Além disso, existem algumas listas importantes que envolvem direções, as quais são usadas para determinar para qual lado será a curva do rio, gerada de maneira aleatória. Exemplo de utilização de listas para armazenar animações dos animais:

```py
for k in range(num_animais):
	direita = []
    esquerda = []
    cima = []
    baixo = []
    for i in range(num_frames):
        baixo.append(pg.transform.smoothscale(pg.image.load(f'assets/animal{k + 1}_baixo{i + 1}.png'), (50, 50)))
        cima.append(pg.transform.smoothscale(pg.image.load(f'assets/animal{k + 1}_cima{i + 1}.png'), (37, 55)))
        direita.append(pg.transform.smoothscale(pg.image.load(f'assets/animal{k + 1}_direita{i + 1}.png'), (55, 55)))
        esquerda.append(pg.transform.smoothscale(pg.image.load(f'assets/animal{k + 1}_esquerda{i + 1}.png'), (55, 55)))
```

- **Funções**: É crucial que em qualquer código minimamente complexo haja definição de funções até para fazer com que o código principal se mantenha limpo e inteligível. No nosso caso, definimo-las em um arquivo a parte, contendo funções que envolvem todos os tipos de colisão, uma função que cria as bordas do rio e outra que cria os poderes na tela. Exemplo da utilização de funções para desenhar objetos na tela, nesse caso, os poderes:

```py
def draw(self,janela, offset_x, offset_y):
        projetil_padrao = pg.transform.scale(self.frames[self.estagio], (70,40))
        projetil_left = pg.transform.flip(projetil_padrao, True, False) #espelha a imagem
        projetil_up = pg.transform.rotate(projetil_padrao, 90) #rotaciona a imagem
        projetil_down = pg.transform.rotate(projetil_padrao, 270) #rotaciona a imagem

        if self.facing_x == 1:
            janela.blit(projetil_padrao, (self.x - offset_x, self.y - offset_y))
        if self.facing_x == -1:
            janela.blit(projetil_left, (self.x - offset_x, self.y - offset_y))
        if self.facing_y == -1:
            janela.blit(projetil_up, (self.x - offset_x, self.y - offset_y))
        if self.facing_y == 1:
            janela.blit(projetil_down, (self.x - offset_x, self.y - offset_y))

        self.estagio += 1
        if self.estagio == len(self.frames):
            self.estagio = 0
```
- **Dicionários e tuplas**: Os dicionários foram utilizados para armazenar os diferentes tipos de animais e suas características, como velocidade, imagem e animações correspondentes, diferentes tipos de poderes e suas imagens, além de detalhes visuais presentes no mapa. As tuplas foram usadas majoritariamente para representar a coordenada de algum objeto, como o mago ou algum animal, as quais foram utilizadas em várias funções embutidas na biblioteca Pygame que possuem uma tupla como um de seus parâmetros. Utilização de dicionários para armazenar características de objetos:

```py
self.poderes_chao = {
            'Coletavel 1': 'poder1', #fogo
            'Coletavel 4': 'tempo',
            'Coletavel 3': 'vida',
            'Coletavel 2': 'poder2' #diminui a velocidade do animal
        }

self.animals =  {
                "Animal 1": {'velocidade': 0.05, 'referencia': {}},
                "Animal 2": {'velocidade': 0.0575, 'referencia': {}},
                "Animal 3": {'velocidade': 0.065, 'referencia': {}}
        }
```
- **Orientação a Objetos (POO)**: Esse foi um dos conceitos mais utilizados durante toda a execução do projeto, uma vez que para a existência de qualquer jogo, é necessário criar objetos na tela e a maneira mais fácil e intuitiva de realizar isso é através da utilização da programação orientada a objetos. Nós usamos esse conceito para criar os animais, tanto os coelhos quanto o dragão, os poderes, o mago, o rio, os projéteis que saem tanto do mago quanto do dragão e as paredes. Exemplo da utilização desse conceito na criação da classe do mago:

```py
class Mago:
    def __init__(self, velocidade, stamina, rios, cooldown_habilidade, vida, largura_mapa, altura_mapa):
        w = largura_mapa
        h = altura_mapa
        self.largura = w / 25.6
        self.altura = h / 14.4
        escolheu = False
        while not escolheu:
            escolheu = True
            self.x = random.randrange(0, LARGURA, 50)
            self.y = random.randrange(100, ALTURA, 50)
            for rio in rios:
                if colisao_amigavel(self, rio):
                    escolheu = False
        self.velocidade = velocidade
        self.stamina = stamina
        self.vida = vida
        self.cooldown_habilidade = cooldown_habilidade
        self.cansaco = 0
        self.img = pg.image.load('assets/mago_down.png')
        self.raio = 300
        self.poder = False
```
## Desafios e erros

1. **Falta de planejamento inicial:** No início do projeto, enfrentamos dificuldades devido à falta de um planejamento sólido. Em vez de seguir um plano bem definido, começamos de forma improvisada, o que resultou em confusão e falta de direção. Como resultado, muitos aspectos do projeto foram realizados com muita pressa, levando a atrasos e retrabalho.
2. **Dificuldades com o GitHub:** A colaboração eficaz no GitHub é crucial para o desenvolvimento de software em equipe. No entanto, muitos membros da equipe não estavam familiarizados com essa plataforma e não tinham conhecimento suficiente para utilizá-la adequadamente. Isso levou a problemas de conflitos de código e dificuldades na coordenação do trabalho.
3. **Desafios na Programação em Equipe:** Trabalhar em equipe apresentou desafios significativos. Embora tenhamos usado ferramentas como Live Share e Discord para facilitar a comunicação, a coordenação das atividades de diferentes membros da equipe foi complicada.
4. **Dificuldades com Pixel Art:** A criação de pixel art se revelou uma tarefa desafiadora para nossa equipe. Encontrar recursos adequados, como tutoriais e ferramentas especializadas, foi um obstáculo, e muitos de nós não tinham experiência prévia nessa área. Como resultado, o processo de criação foi bem mais demorado do que o esperado.
5. **Aplicação de conceitos:** Outro desafio que enfrentamos foi a necessidade de aplicar todos os conceitos e habilidades que havíamos aprendido ao longo do semestre. Embora tivéssemos abordado diferentes aspectos do projeto separadamente, integrar todos os elementos em um produto final foi complexo. Isso exigiu um esforço adicional para garantir que todas as partes funcionassem em conjunto de maneira adequada.

## Links importantes

[Animação dos animais aparecendo e desaparecendo](https://nyknck.itch.io/fx062)

[Árvores, enfeites e detalhes do mapa](https://cupnooble.itch.io/sprout-lands-asset-pack)

[Animações dos poderes](https://bdragon1727.itch.io/fire-pixel-bullet-16x16)

[Animações do mago](https://flandrescarlet64.itch.io/16x16-16-bits-top-down-mage-character)

[Animações dos animais](https://www.rpgmakercentral.com/topic/2399-grannys-lists-animal-sprites/)

[Animações do dragão](https://br.pinterest.com/pin/811351689095548879/)

[Menu de informações do jogo](https://stock.adobe.com/br/images/pixel-art-wood-style-button-for-game-and-app-interface-vector-icon-for-8bit-game-on-white-background/512472259)

[Sons](https://mixkit.co/free-sound-effects/magic/?page=2)

[Mais sons](https://audiojungle.net/item/ice-crackling/23170883?s_rank=1)


## Capturas de tela

<p align="center">
  <img src="https://github.com/thomazcabral/ProjetoIP/blob/afea2831d400149f54a1b935c960cda53f7ce124/assets/Screenshot%20(2).png">
  <img src="https://github.com/thomazcabral/ProjetoIP/blob/afea2831d400149f54a1b935c960cda53f7ce124/assets/Screenshot%20(8).png">
  <img src="https://github.com/thomazcabral/ProjetoIP/blob/afea2831d400149f54a1b935c960cda53f7ce124/assets/Screenshot%20(7).png">
	
</p>
