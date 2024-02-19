
# The Forest Mage

This project consists of a 2D game created using the Python programming language and the Pygame library. It was developed as part of the Introduction to Programming (IP) course offered at CIn-UFPE.

## Game Mechanics

- Installation of the latest version of Python;
- Installation of the Pygame library using the command pip install pygame;
- Installation of the numpy library using the command pip install numpy.

## Participants

- [Diana Rocha Silva](https://github.com/Diana-RS)
- [Filip Pawlowski Augusto Fernandes](https://github.com/filip-fernandes)
- [João Luís da Silva Marrocos](https://github.com/jlsm2)
- [Pedro Henrique Moraes de Sousa Silva](https://github.com/pedroagaeme)
- [Thomaz Cabral Corrêa de Araújo](https://github.com/thomazcabral)

## Ideation and Objectives

The main idea of the team was to create a top-down perspective game, where the camera and perspective allow the player to observe the environment and characters from an aerial view, usually from top to bottom. Another idea was to create a collecting game, where a main character would move towards other objects that would try to stay away from the main character. For the visual creation of the game, it took us some time to come up with a good and applicable idea until we were inspired by the game "Stardew Valley", a simulation of a character performing actions in a bucolic environment. However, the visual resources of the game were gradually altered until the visual identity became significantly different from that other game.

In general, the game consists of a mage whose objective is to escape from the dragon, which can be eliminated later, and collect as many animals as possible within a determined period of time. The mage can collect the animals by touching them or by using powers, which are special abilities of the mage that appear on the map. Among these powers, we have instant collection of animals, temporary slowing down of animals, increase in the amount of available time, and elevation of the mage's life. The map is composed of randomly generated tiles (squares), so each time someone plays, the generated map is different. It is also decorated with trees, leaves, flowers, fruits, mushrooms, and a river. At the bottom of the game, there is an information menu about the current game, showing the mage's life and stamina, the power the mage collected and is ready to be used, as well as the counter of how many animals have been collected. It is of utmost importance to highlight the existence of an initial menu, which allows the player to start or quit the game, and a final menu, which displays the player's score, offers the possibility of quitting the game, or starting another game. If the player loses his life due to damage received by the dragon, he is declared defeated. Otherwise, his score will appear on the screen.

## Project Architecture

The entire code was divided into the following parts in order to make it more intuitive and understandable:

- **Assets**: Folder containing all the images displayed in the game, including the animals and their respective sprites, the menu background, details shown on the game map such as mushrooms, flowers, leaves, and fruits, projectiles launched by both the mage and the dragon, wood that constitutes the menu where useful game information appears, powers that appear on the map, the map tiles, the bridge, and the river, as well as the trees and fonts used in the program.
- **Classes**: Folder where the objects and their actions present in the game are located, in a completely object-oriented environment (OOP). Among the functions found in this location, we have: the movement and random appearance of animals and the mage, and the creation of all objects on the screen.
- **Functions**: File where all the functions used in the main code are defined: collision of the mage with the edge, collision of the mage with animals, collision of the mage with powers, and collision of objects with walls, preventing them from following their natural movement, as well as a function involving the creation of the river.
- **Config**: File where constants are defined, such as colors, screen size settings, quantity of animals, speed of animals and mage, as well as general map settings.
- **Engine**: Main part of the code, which makes the game enter a loop and function correctly. It is important to note that this part contained in the "Engine" class is completely worked in OOP. It is in this segment that objects are created, rendered, where the timer is created, and the number of collected animals is counted.
- **Main**: Small piece of code, which ensures that a specific block of code is executed only when the Python script is executed directly as the main program and not when it is imported as a module into another script.

## Libraries and Tools

- **Pygame**: Library used to create and make the game work. We used its various functions such as functions to draw on the screen, create windows, establish the font of a certain text, implement images in the game, and terminate the program.
- **Sys**: Library used only to terminate the program.
- **Time**: Library used to create and display a timer on the screen, which shows the user how much game time he has until the game ends.
- **Random**: As the game map is generated randomly, meaning that every time someone plays, the dynamics and visual of the game will be completely different, this library was widely used for this function, choosing random numbers and images to improve the program's gameplay, as well as choosing the direction when the animals are not close to the mage. It was most used in the random generation of rivers, in the generation of trees, and in the position of the animals.

## Work Division

- Diana: creation of pixel arts, elaboration of the initial and final menu, code modularization.
- Filip: code restructuring, creation of certain functions in classes.
- João: creation of projectiles, animations, and game information menu, dragon ornamentation.
- Pedro: project ideation, creation of animals, river, and map randomness, implementation of arts.
- Thomaz: dragon creation, OOP implementation, report, and presentation elaboration.

It is worth mentioning that everyone managed to practice what was learned in the course during the semester, and this project was entirely carried out together, with everyone understanding what was done according to the proper planning.

## Concepts in Practice

- **Conditionals**: The code section where conditional statements were most used is in the collision checking between the characters and between them and the existing walls, which consist of the border of the window where the game runs, the trees, and the river. Specifically, we used conditionals due to the need to compare the position (x and y) of the objects so that the object cannot move anymore if it tries or it disappears, in the case of the collision of the mage with the animals he hunts. In addition, they were also used to check the last key pressed by the user so that the power is not thrown in the wrong direction and to avoid possible problems in the mage's movement. For updating the life and stamina bars, their decrease when the character takes damage and spends his energy, respectively, conditional propositions were also used. Example of conditional use for the correct operation of the camera:

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

- **Looping Structures**: They were extensively used to check collision between all objects existing in the program and were also useful for iterating over each animal and calling the function that moves them, creating blocks so that the mage can spawn far from the animals and powers and cannot spawn in trees or in the river. The program's main loop and the random generation of rivers also work due to looping structures. Example of the use of this tool to iterate over lists of objects to apply collision:

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
- **Lists**: Lists were used to store live and already collected animals, projectiles appearing on the map, each existing tilemap, the current game's river, and the powers displayed on the map. In addition, there are some important lists involving directions, which are used to determine which direction the river curve will be, randomly generated. Example of using lists to store animal animations:

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

- **Functions**: It is crucial that in any minimally complex code, there are function definitions even to keep the main code clean and understandable. In our case, we defined them in a separate file, containing functions involving all types of collision, a function that creates the river borders, and another that creates the powers on the screen. Example of using functions to draw objects on the screen, in this case, the powers:

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
- **Dictionaries and Tuples**: Dictionaries were used to store different types of animals and their characteristics, such as speed, image, and corresponding animations, different types of powers and their images, as well as visual details present on the map. Tuples were used mainly to represent the coordinate of some object, such as the mage or some animal, which were used in various built-in functions of the Pygame library that have a tuple as one of their parameters. Use of dictionaries to store object characteristics:

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
- **Object-Oriented Programming (OOP)**: This was one of the most used concepts throughout the project execution, as for the existence of any game, it is necessary to create objects on the screen and the easiest and most intuitive way to do this is through the use of object-oriented programming. We used this concept to create the animals, both rabbits and the dragon, the powers, the mage, the river, the projectiles that come from both the mage and the dragon, and the walls. Example of using this concept in creating the mage class:

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
## Challenges and Mistakes

1. **Lack of Initial Planning:** At the beginning of the project, we faced difficulties due to the lack of solid planning. Instead of following a well-defined plan, we started in an improvised manner, resulting in confusion and lack of direction. As a result, many aspects of the project were rushed, leading to delays and rework.
2. **Issues with GitHub:** Effective collaboration on GitHub is crucial for team software development. However, many team members were not familiar with this platform and lacked sufficient knowledge to use it properly. This led to code conflicts and difficulties in coordinating work.
3. **Challenges in Team Programming:** Working in a team presented significant challenges. Although we used tools like Live Share and Discord to facilitate communication, coordinating the activities of different team members was complicated.
4. **Difficulties with Pixel Art:** Creating pixel art proved to be a challenging task for our team. Finding suitable resources such as tutorials and specialized tools was an obstacle, and many of us lacked prior experience in this area. As a result, the creation process took much longer than expected.
5. **Application of Concepts:** Another challenge we faced was the need to apply all the concepts and skills we had learned throughout the semester. Although we had addressed different aspects of the project separately, integrating all elements into a final product was complex. This required additional effort to ensure that all parts worked together properly.

## Important Links

[Animation of animals appearing and disappearing](https://nyknck.itch.io/fx062)

[Trees, ornaments, and map details](https://cupnooble.itch.io/sprout-lands-asset-pack)

[Power animations](https://bdragon1727.itch.io/fire-pixel-bullet-16x16)

[Mage animations](https://flandrescarlet64.itch.io/16x16-16-bits-top-down-mage-character)

[Animal animations](https://www.rpgmakercentral.com/topic/2399-grannys-lists-animal-sprites/)

[Dragon animations](https://br.pinterest.com/pin/811351689095548879/)

[Game information menu](https://stock.adobe.com/br/images/pixel-art-wood-style-button-for-game-and-app-interface-vector-icon-for-8bit-game-on-white-background/512472259)

[Sounds](https://mixkit.co/free-sound-effects/magic/?page=2)

[More sounds](https://audiojungle.net/item/ice-crackling/23170883?s_rank=1)


## Screenshots

<p align="center">
  <img src="https://github.com/thomazcabral/ProjetoIP/blob/afea2831d400149f54a1b935c960cda53f7ce124/assets/Screenshot%20(2).png">
  <img src="https://github.com/thomazcabral/ProjetoIP/blob/afea2831d400149f54a1b935c960cda53f7ce124/assets/Screenshot%20(8).png">
  <img src="https://github.com/thomazcabral/ProjetoIP/blob/afea2831d400149f54a1b935c960cda53f7ce124/assets/Screenshot%20(7).png">
	
</p>
