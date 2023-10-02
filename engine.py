import pygame as pg
import sys
import time
import random
from classes.utilidades import *
from classes import Animais, Parede, Mago, Rio, Projectile, Projectile_hud, Dragao, functions, Menu, Coletaveis, Animacao, PauseMenu, GameoverMenu
from copy import deepcopy

class Engine:
    def __init__(self, config: dict) -> None:
        self.global_config = config
        self.screen_config = config["screen_config"]
        self.color_config = config["color_config"]
        self.camera_config = config["camera_config"]
        self.animal_config = config["animal_config"]
        self.player_config = config["player_config"]
        self.speed_config = config["speed_config"]
        self.map_config = config["map_config"]
        self.hud_config = config["hud_config"]

        num_frames_animacao = [5, 7, 6]
        self.animacoes = {
            'animacao1': '',
            'animacao2': ''
        }

        for k in range(len(num_frames_animacao)):
            frames_animacao = []
            for i in range(num_frames_animacao[k]):
                img  = (pg.image.load(f"assets/animacao{k + 1}_{i}.png"))
                frames_animacao.append(pg.transform.scale(img, (64, 64)))
            self.animacoes[f'animacao{k +1}'] = frames_animacao


        self.offset_x = 0
        self.offset_y = 0

        self.animals =  {
                "Animal 1": {'velocidade': 0.05, 'referencia': {}},
                "Animal 2": {'velocidade': 0.0575, 'referencia': {}},
                "Animal 3": {'velocidade': 0.065, 'referencia': {}}
        }
        self.animal1_idle =  None
        self.animal2_idle =  None
        self.animal3_idle =  None

        self.dragon = {
            "Dragao": {'referencia': {}}
        }

        self.hud = None
        self.hud_skill = None
        self.hud_skill_cooldown = None
        self.fonte_contador = None
        self.fonte_tempo = None
        self.menu = Menu()
        self.should_restart = False

        # Sobre o mapa
        self.tilemap = []
        self.mapa = {}
        self.desenho_enfeites = []
        self.enfeites = {}

        self.direcoes = ['direita', 'esquerda', 'baixo', 'cima']
        self.direcoes2 = self.direcoes.copy()
        self.foz = False
        self.direcao_rio_inicial = random.choice(self.direcoes)
        self.direcao_rio = self.direcao_rio_inicial

        self.fluxo_rio = None
        self.rio = None

        self.mago = None

        self.num_arvores = random.randint(10, 30)
        self.ponte = False

        self.pontos_animais = {
            'Animal 1': 0,
            'Animal 2': 0,
            'Animal 3': 0,
        }
        self.dragon_kills = 0

        self.poderes = {}
        self.cooldown_poder = 0
        self.tempo_poder = False
        self.frames_fogo = []
        self.num_frames_fogo = 5
        self.num_frames_poder1 = 6
        self.num_frames_poder2 = 6
        self.tipos_poder = 2
        self.poderes_chao = {
            'Coletavel 1': 'poder1', #fogo
            'Coletavel 4': 'tempo',
            'Coletavel 3': 'vida',
            'Coletavel 2': 'poder2' #diminui a velocidade do animal
        }
        self.cooldown = False
        self.cooldown_sprite = False

        self.ratio_stamina = self.player_config["stamina_padrao"] / 1000
        self.ratio_habilidade = self.player_config["cooldown_habilidade_padrao"] / 270
        self.ratio_vida = self.player_config["vida_padrao"] / 1000
        
        self.cargas = []
        self.cargas_hud = []
        self.cargas_dragao = []
        self.vida_dragao = 120

        self.running = True
        self.game_started = False
        self.paused = False

        self.janela = None

        self.x_barras = self.camera_config["largura_camera"] / (self.camera_config["largura_camera"] / 10)
        self.y_barra_stamina = self.camera_config["altura_camera"] / (self.camera_config["altura_camera"]/(self.camera_config["altura_camera"] - 23))
        self.y_barra_vida = self.camera_config["altura_camera"] / (self.camera_config["altura_camera"]/(self.camera_config["altura_camera"] - 39))

        

        self.duracao_timer = 60 
        self.tempo_restante = 60
        self.janela = pg.display.set_mode((self.camera_config["largura_camera"], self.camera_config["altura_camera"]), pg.FULLSCREEN)
        pg.init()

    def run(self) -> None:
        self.should_restart = False
        self.running = True

        self.pause_menu = PauseMenu(self, self.janela)
        self.gameover_menu = GameoverMenu(self, self.janela)

        clock = pg.time.Clock()

        self.clear_game() # Pro caso de restart, limpa o mapa antigo.

        self.load_map()
        self.load_river()
        self.load_mage()
        self.create_trees() 
        self.load_hud()
        self.load_animals()
        self.load_dragon()
        self.load_powers()
        self.spawn_animals()
        self.create_bridges()       

        setas = {'RIGHT': 0, 'LEFT': 0, 'UP': 0, 'DOWN': 0}
        ultima_seta = {'RIGHT': 0, 'LEFT': 0, 'UP': 0, 'DOWN': 0, 'SPACE': 0, 'Q' : 0, 'E' : 0}

        while self.running:
            if not self.game_started:
                # Mostrar janela do menu
                self.menu.show_menu(self.janela)

                # Checar se o jogo deve iniciar
                if self.menu.start_game:
                    self.comeco_timer = time.time() 
                    self.game_started = True  # Iniciou
                    
            else:
                if self.tempo_restante <= 0 or self.mago.vida <= 0:
                    self.gameover_menu.draw()
                    for event in pg.event.get():
                        if self.gameover_menu.handle_event(event):
                            self.run()
                    pg.display.update()
                else:
                    variacao_tempo = clock.tick(30)
                    keys = pg.key.get_pressed() 
                    old_time = deepcopy(self.tempo_restante)
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            self.running = False
                        elif event.type == pg.KEYDOWN:
                            if event.key == pg.K_ESCAPE:
                                if not self.paused:
                                    self.paused = True
                                    self.pause_menu.paused = True
                                    self.pause_menu.toggle()  # Mostrar menu de pausa
                                else:
                                    self.tempo_restante = old_time
                                    self.duracao_timer = old_time
                                    self.comeco_timer = time.time()
                                    self.paused = False
                                    self.pause_menu.paused = False
                                    self.pause_menu.toggle()  # Esconder menu de pausa
                        if self.paused:
                            self.pause_menu.draw()
                            self.pause_menu.handle_event(event, old_time)
                            pg.display.update()
                    if self.paused:
                        continue

                    self.align_camera(
                        largura_camera=self.camera_config["largura_camera"],
                        altura_camera=self.camera_config["altura_camera"]
                    )
                    for evento in pg.event.get():
                        if evento.type == pg.QUIT:
                            self.running = False
                    if ultima_seta['SPACE'] == 0:
                        self.cooldown = False
                        self.cooldown_sprite = False
                    else:
                        self.cooldown_sprite = True
                    

                    if not self.cooldown:
                        self.check_power_colision()
                    self.check_dragon_fire_colision()
                    self.try_spawning_dragon()

                    self.render_map()
                    self.render_trunk()
                    self.render_collectables()
                    self.render_animations()
                    self.render_entities()
                    self.render_projectile(keys, ultima_seta)
                    self.render_mage()
                    self.render_leaves()
                    self.render_dragon()
                    self.render_hud()
                    

                    self.mago.move(keys, variacao_tempo, setas, ultima_seta, Parede.paredes, Rio.rios)
                    self.move_animal(variacao_tempo)
                    self.move_dragon(variacao_tempo)
        
                    self.janela.blit(self.janela, (0,0)) #atualiza o timer e as barras corretamente
                    pg.display.update()
            
            if self.should_restart:
                self.run()
    
    def load_mage(self):
        self.mago = Mago(
            self.speed_config["velocidade_padrao"], 
            self.player_config["stamina_padrao"], 
            Rio.rios, 
            self.player_config["cooldown_habilidade_padrao"], 
            self.player_config["vida_padrao"],
            self.screen_config["LARGURA_MAPA"],
            self.screen_config["ALTURA_MAPA"]
        )
    
    def load_animals(self) -> None:
        num_animais = self.animal_config["num_animais"]
        num_frames = self.animal_config["num_frames"]
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
            self.animals[f'Animal {k + 1}']['referencia']['esquerda'] = esquerda
            self.animals[f'Animal {k + 1}']['referencia']['direita'] = direita
            self.animals[f'Animal {k + 1}']['referencia']['cima'] = cima
            self.animals[f'Animal {k + 1}']['referencia']['baixo'] = baixo
        self.animal1_idle =  self.animals['Animal 1']['referencia']['baixo'][0]
        self.animal2_idle =  self.animals['Animal 2']['referencia']['baixo'][0]
        self.animal3_idle =  self.animals['Animal 3']['referencia']['baixo'][0]
    
    def load_dragon(self) -> None:
        num_frames = self.animal_config["num_frames"]
        direita_dragao = []
        esquerda_dragao = []
        cima_dragao = []
        baixo_dragao = []
        for i in range(num_frames):
            baixo_dragao.append(pg.transform.smoothscale(pg.image.load(f'assets/dragao_baixo_{i + 1}.png'), (198, 128)))
            cima_dragao.append(pg.transform.smoothscale(pg.image.load(f'assets/dragao_cima_{i + 1}.png'), (198, 128)))
            direita_dragao.append(pg.transform.smoothscale(pg.image.load(f'assets/dragao_direita_{i + 1}.png'), (198, 128)))
            esquerda_dragao.append(pg.transform.smoothscale(pg.image.load(f'assets/dragao_esquerda_{i + 1}.png'), (198, 128)))

        self.dragon['Dragao']['referencia']['baixo'] = baixo_dragao
        self.dragon['Dragao']['referencia']['cima'] = cima_dragao
        self.dragon['Dragao']['referencia']['direita'] = direita_dragao
        self.dragon['Dragao']['referencia']['esquerda'] = esquerda_dragao


        for i in range(self.num_frames_fogo):
            self.frames_fogo.append(pg.image.load(f'assets/fogo{i + 1}.png'))
    
    def load_hud(self) -> None:
        # Carregar fontes e imagens
        self.hud = pg.transform.scale(pg.image.load('assets/hud.png'), (1800, 70)) #imagem da madeira do menu inferior
        self.fonte_contador = pg.font.Font('assets/CW_BITMP.ttf', 24) #fonte importada para o menu inferior
        self.fonte_tempo = pg.font.Font('assets/CW_BITMP.ttf', 24)
    
    def load_map(self) -> None:
        num_tiles = self.map_config["num_tiles"]
        num_enfeites = self.map_config["num_enfeites"]
        map_width = self.screen_config["LARGURA_MAPA"]
        map_height = self.screen_config["ALTURA_MAPA"]
        for i in range(num_tiles):
            self.tilemap.append(pg.transform.scale(pg.image.load(f'assets/tile{i + 1}.png'), (50, 50)))
        for j in range(num_enfeites):
            self.desenho_enfeites.append(pg.transform.scale(pg.image.load(f'assets/enfeite{j + 1}.png'), (50, 50)))
        for x in range(0, map_width, 50):
            for y in range(0, map_height, 50):
                aleatorio = random.randint(1,10)
                if aleatorio == 1:
                    numero = random.randint(2, 13)
                else:
                    numero = 1
                self.mapa[(x, y)] = numero
    
    def load_river(self) -> None:
        map_width = self.screen_config["LARGURA_MAPA"]
        map_height = self.screen_config["ALTURA_MAPA"]
        if self.direcao_rio_inicial == 'direita':
            y = random.randrange(0, map_height, 100)
            if y > (map_height / 2):
                direcao_rio_final = 'cima'
            else:
                direcao_rio_final = 'baixo'
            self.mapa[(0, y)] = self.mapa[(50, y)] = self.mapa[(0, y + 50)] = self.mapa[(50, y + 50)] = 14
            x_vez = 0
            y_vez = y
        elif self.direcao_rio_inicial == 'esquerda':
            y = random.randrange(0, map_height, 100)
            if y > (map_height / 2):
                direcao_rio_final = 'cima'
            else:
                direcao_rio_final = 'baixo'
            ultimo = map_width
            while ultimo % 50 != 0:
                ultimo -= 1
            ultimo -= 50
            self.mapa[(ultimo, y)] = self.mapa[(ultimo + 50, y)] = self.mapa[(ultimo, y + 50)] = self.mapa[(ultimo + 50, y + 50)] = 14
            x_vez = ultimo
            y_vez = y
        elif self.direcao_rio_inicial == 'baixo':
            x = random.randrange(0, map_width, 100)
            if x > (map_width / 2):
                direcao_rio_final = 'esquerda'
            else:
                direcao_rio_final = 'direita'
            self.mapa[(x, 0)] = self.mapa[(x, 50)] = self.mapa[(x + 50, 0)] = self.mapa[(x + 50, 50)] = 14
            x_vez = x
            y_vez = 0
        elif self.direcao_rio_inicial == 'cima':
            x = random.randrange(0, map_width, 100)
            if x > (map_width / 2):
                direcao_rio_final = 'esquerda'
            else:
                direcao_rio_final = 'direita'
            ultimo = map_height
            while ultimo % 50 != 0:
                ultimo -= 1
            ultimo -= 50
            self.mapa[(x, ultimo)] = self.mapa[(x, ultimo + 50)] = self.mapa[(x + 50, ultimo)] = self.mapa[(x + 50, ultimo + 50)] = 14
            x_vez = x
            y_vez = ultimo
        self.fluxo_rio = [self.direcao_rio_inicial, direcao_rio_final]
        self.rio = Rio(x_vez, y_vez)
        functions.contorno_rio(self.mapa, x_vez, y_vez)
        foz = False
        while not foz:
            self.direcao_rio = random.choice(self.fluxo_rio)
            if self.direcao_rio == 'direita':
                x_vez += 100
                if x_vez + 150 > map_width:
                    foz = True
                self.mapa[(x_vez, y_vez)] = self.mapa[(x_vez, y_vez + 50)] = self.mapa[(x_vez + 50, y_vez)] = self.mapa[(x_vez + 50, y_vez + 50)] = 14
            elif self.direcao_rio == 'esquerda':
                x_vez -= 100
                if x_vez <= 0:
                    foz = True
                self.mapa[(x_vez, y_vez)] = self.mapa[(x_vez, y_vez + 50)] = self.mapa[(x_vez + 50, y_vez)] = self.mapa[(x_vez + 50, y_vez + 50)] = 14
            elif self.direcao_rio == 'baixo':
                y_vez += 100
                if y_vez + 100 > map_height:
                    foz = True
                self.mapa[(x_vez, y_vez)] = self.mapa[(x_vez, y_vez + 50)] = self.mapa[(x_vez + 50, y_vez)] = self.mapa[(x_vez + 50, y_vez + 50)] = 14
            elif self.direcao_rio == 'cima':
                y_vez -= 100
                if y_vez <= 0:
                    foz = True
                self.mapa[(x_vez, y_vez)] = self.mapa[(x_vez, y_vez + 50)] = self.mapa[(x_vez + 50, y_vez)] = self.mapa[(x_vez + 50, y_vez + 50)] = 14
            functions.contorno_rio(self.mapa, x_vez, y_vez)
            self.rio = Rio(x_vez, y_vez)

        for x in range(0, map_width, 50):
            for y in range(0, map_height, 50):
                if self.mapa[(x, y)] == 1:
                    num = random.randint(1, 30)
                    if num == 1:
                        aleatorio = random.randint(1, 11)
                        posicao_x = random.randint(x, x + 25)
                        posicao_y = random.randint(y, y + 25)
                        self.enfeites[(x, y)] = (aleatorio, (posicao_x, posicao_y))
        
        for (x, y) in self.mapa.keys():
            if (x + 50, y) in self.mapa.keys() and (x, y + 50) in self.mapa.keys():
                if self.mapa[((x + 50, y))] == 18 and self.mapa[((x, y + 50))] == 19:
                    self.mapa[(x, y)] = 24
                    self.mapa[(x + 50, y + 50)] = 28
            if (x - 50, y) in self.mapa.keys() and (x, y + 50) in self.mapa.keys():
                if self.mapa[((x - 50, y))] == 18 and self.mapa[((x, y + 50))] == 17:
                    self.mapa[(x, y)] = 25
                    self.mapa[(x - 50, y + 50)] = 31
            if (x + 50, y) in self.mapa.keys() and (x, y - 50) in self.mapa.keys():
                if self.mapa[((x + 50, y))] == 16 and self.mapa[((x, y - 50))] == 19:
                    self.mapa[(x, y)] = 26
                    self.mapa[(x + 50, y - 50)] = 29
            if (x - 50, y) in self.mapa.keys() and (x, y - 50) in self.mapa.keys():
                if self.mapa[((x - 50, y))] == 16 and self.mapa[((x, y - 50))] == 17:
                    self.mapa[(x, y)] = 27
                    self.mapa[(x - 50, y - 50)] = 30

    def create_trees(self) -> None:
        #cria as arvores
        for j in range(self.num_arvores):
            Parede(
                0.05, 
                self.mago, 
                Rio.rios, 
                self.screen_config["LARGURA_MAPA"], 
                self.screen_config["ALTURA_MAPA"]            
            )
    
    def create_bridges(self) -> None:
        while not self.ponte:
            bloco = random.choice(Rio.rios)
            if (bloco.x - 100, bloco.y) in self.mapa.keys() and (bloco.x + 100, bloco.y) in self.mapa.keys():
                self.ponte = True
                for rio in Rio.rios:
                    if (bloco.x - 100, bloco.y) == (rio.x, rio.y) or (bloco.x + 100, bloco.y) == (rio.x, rio.y):
                        self.ponte = False
                if self.ponte:
                    print("AAAAAAAAAAAAAAAAAAA")
                    bloco.construir_ponte(self.mapa)

    def spawn_animals(self) -> None:
        for animal in self.animals.keys():
            self.pontos_animais[animal] = 0
        for i in range(self.animal_config["num_animais"]):
            nome = random.choice([k for k in self.animals.keys()])
            Animais(self.animals, nome, self.mago, self.animacoes)
        for animal in Animais.animais_vivos:
            animal.spawnar(
                self.mago, 
                Parede.paredes, 
                Rio.rios, 
                Dragao.dragoes_vivos, 
                self.offset_x, 
                self.offset_y
            )

    def load_powers(self):
        for k in range(self.tipos_poder):
            frames_poder = []
            for i in range(self.num_frames_poder2):
                frames_poder.append(pg.image.load(f'assets/projetil{k + 1}_{i}.png'))
            self.poderes[f'poder{k + 1}'] = frames_poder

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

    def check_power_colision(self) -> None:
        for poder in self.cargas:
            if self.offset_x - 40 <= poder.x < self.camera_config["largura_camera"] + self.offset_x:
                poder.x += poder.vel_x
            else:
                self.cargas.pop(self.cargas.index(poder))
            if self.offset_y - 60 <= poder.y < self.camera_config["altura_camera"] + self.offset_y:
                poder.y += poder.vel_y
            else:
                self.cargas.pop(self.cargas.index(poder))
            #checando colisão com animais
            for animal in Animais.animais_vivos:
                if functions.colisao_amigavel(poder, animal):
                    functions.colisao_poder(poder, animal, self.pontos_animais)
                    self.cargas.pop(self.cargas.index(poder))

            #checando colisão com animais
            for dragao in Dragao.dragoes_vivos:
                if functions.colisao_amigavel(poder, dragao):
                    if functions.colisao_dragao(poder, dragao):
                        self.dragon_kills += 1
                    self.cargas.pop(self.cargas.index(poder))

            #checando colisão com paredes        
            for parede in Parede.paredes:
                if functions.colisao_amigavel(poder, parede):
                    self.cargas.pop(self.cargas.index(poder))
    
    def check_dragon_fire_colision(self):
        for poder in self.cargas_dragao:
            if self.offset_x - 40 <= poder.x < self.camera_config["largura_camera"] + self.offset_x:
                poder.x += poder.vel_x
            else:
                self.cargas_dragao.pop(self.cargas_dragao.index(poder))
            if self.offset_y - 60 <= poder.y < self.camera_config["altura_camera"] + self.offset_y:
                poder.y += poder.vel_y
            else:
                self.cargas_dragao.pop(self.cargas_dragao.index(poder))
            #checando colisão com animais
            if functions.colisao_amigavel(poder, self.mago):
                self.mago.vida -= 250
                if self.mago.vida < 0:
                    self.mago.vida = 0
                self.cargas_dragao.pop(self.cargas_dragao.index(poder))

            #checando colisão com paredes 
            try:
                for parede in Parede.paredes:
                    if functions.colisao_amigavel(poder, parede):
                        self.cargas_dragao.pop(self.cargas_dragao.index(poder))
            except:
                pass

    
    def try_spawning_dragon(self):
        if len(Dragao.dragoes_vivos) < 1:
            dragao = Dragao(self.speed_config["velocidade_padrao"], "Dragao", self.mago, self.vida_dragao, self.dragon, self.frames_fogo)
            dragao.spawnar(self.mago, Parede.paredes, Rio.rios,  self.screen_config["LARGURA_MAPA"], self.screen_config["ALTURA_MAPA"])

    def render_collectables(self):
        chance = random.randint(1, 10) #mudar o 200
        total_poderes = len(Coletaveis.coletaveis_ativos)
        for coletavel in Coletaveis.coletaveis_ativos:
            tempo_aumentado = functions.colisao_coleta(self.mago, coletavel)
            if tempo_aumentado:
                self.duracao_timer += tempo_aumentado
        if total_poderes == 0 or (chance == 1 and total_poderes <= 10): 
            nome = self.poderes_chao[f"Coletavel {random.randint(1,4)}"]
            coletavel = Coletaveis(nome)
            coletavel.spawnar(self.mago, Parede.paredes, Rio.rios, Dragao.dragoes_vivos, Animais.animais_vivos, self.screen_config["LARGURA_MAPA"], self.screen_config["ALTURA_MAPA"])
         # Renderizar coletáveis
        for coletavel in Coletaveis.coletaveis_ativos:
            coletavel.desenhar_coletavel(self.janela, self.offset_x, self.offset_y)

    def move_animal(self, variacao_tempo):
        for animal in Animais.animais_vivos:
            animal.move(self.mago, variacao_tempo, Parede.paredes, Rio.rios, Dragao.dragoes_vivos, self.speed_config["velocidade_devagar"], self.speed_config["velocidade_rapida"])
        # Colisão com as bordas
        self.mago = functions.borda(self.mago, self.screen_config["LARGURA_MAPA"], self.screen_config["ALTURA_MAPA"])
        for animal in Animais.animais_vivos: 
            animal = functions.colisao(self.mago, animal, self.pontos_animais)
    
    def move_dragon(self, variacao_tempo):
        # Movimentação do dragao
        for dragao in Dragao.dragoes_vivos:
            dragao.move(self.mago, variacao_tempo, Parede.paredes, Rio.rios, self.speed_config["velocidade_devagar"], self.speed_config["velocidade_rapida"], self.cargas_dragao)

        # Colisão do dragao com o mago
        for dragao in Dragao.dragoes_vivos:  
            dragao = functions.dano_dragao(self.mago, dragao)


    def render_entities(self):
        # Renderizar animais
        chance = random.randint(1, 200)
        total_vivos = len(Animais.animais_vivos)
        nenhum = True
        for animal in Animais.animais_vivos:
            if not (animal.x < self.offset_x - animal.largura or animal.x >= self.offset_x + self.camera_config["largura_camera"] or animal.y < self.offset_y - animal.altura or animal.y > self.offset_y + altura_camera):
                nenhum = False
        if nenhum or total_vivos == 0 or (chance == 1 and total_vivos <= 20): 
            nome = random.choice([j for j in self.animals.keys()])
            new_animal = Animais(self.animals, nome, self.mago, self.animacoes)
            new_animal.spawnar(self.mago, Parede.paredes, Rio.rios, Dragao.dragoes_vivos, self.offset_x, self.offset_y)
        for animal in Animais.animais_vivos:
            animal.desenhar_animal(self.janela, self.offset_x, self.offset_y)

        # Renderizar poderes
        if not self.cooldown:
            functions.draw_poder(self.cargas, self.janela, self.offset_x, self.offset_y)
        functions.draw_poder(self.cargas_dragao, self.janela, self.offset_x, self.offset_y)
    
    def render_dragon(self):
        # Renderizar dragão e sua vida
        for dragao in Dragao.dragoes_vivos: #desenhando o dragao
            dragao.desenhar_dragao(janela, self.offset_x, self.offset_y)
        for dragao in Dragao.dragoes_vivos:
            pg.draw.rect(
                self.janela, 
                self.color_config["CINZA"], 
                (
                    dragao.x + 33 - self.offset_x, 
                    dragao.y - self.offset_y, 
                    120, 
                    10
                ), 
                border_radius=self.hud_config["raio_borda"] + 10
            )

            pg.draw.rect(
                self.janela, 
                self.color_config["VERMELHO"], 
                (
                    dragao.x + 33 - self.offset_x, 
                    dragao.y - self.offset_y, 
                    dragao.vida, 
                    10
                ), 
                border_radius=self.hud_config["raio_borda"] + 10
            )

            pg.draw.rect(
                janela, 
                self.color_config["MARROM_ESCURO"], 
                (
                    dragao.x + 33 - self.offset_x, 
                    dragao.y - self.offset_y, 
                    120, 
                    10 
                ), self.hud_config["espessura"] + 1, 
                border_radius=self.hud_config["raio_borda"] + 10
            )

    def render_animations(self):
        #renderiza as animações de desaparecimento ds animais
        for animacao in Animacao.animacoes_ativas:
            animacao.rodar(janela, self.offset_x, self.offset_y)

    def render_projectile(self, keys, ultima_seta):
        if self.mago.poder:
            if keys[pg.K_SPACE]:
                if not self.tempo_poder:
                    self.tempo_poder = 100
                if self.tempo_poder > 0 and self.cooldown_poder == 0:
                    self.cooldown_poder = 20
                    if ultima_seta['LEFT'] != 0:
                        facing_x = -1
                        facing_y = 0
                    elif ultima_seta['RIGHT'] != 0:
                        facing_x = 1
                        facing_y = 0
                    elif ultima_seta['UP'] != 0:
                        facing_y = -1
                        facing_x = 0
                    else:
                        facing_y = 1
                        facing_x = 0
                    self.cargas.append(Projectile(self.mago.x + self.mago.largura / 2 , self.mago.y + self.mago.altura / 2, 4, facing_x, facing_y, self.mago.poder, self.poderes[self.mago.poder]))
            if self.tempo_poder:
                self.tempo_poder -=1
                if self.cooldown_poder > 0:
                    self.cooldown_poder -= 1
                if self.tempo_poder <= 0:
                    self.tempo_poder = False
                    self.mago.poder = False

    def render_map(self):
        largura_mapa = self.screen_config["LARGURA_MAPA"]
        altura_mapa = self.screen_config["ALTURA_MAPA"]
        for x in range(0, largura_mapa, 50):
            for y in range(0, altura_mapa, 50):
                self.janela.blit(self.tilemap[self.mapa[(x, y)] - 1], (x - self.offset_x, y - self.offset_y))
        for x in range(0, largura_mapa, 50):
            for y in range(0, altura_mapa, 50):
                if (x, y) in self.enfeites.keys():
                    self.janela.blit(self.desenho_enfeites[self.enfeites[(x, y)][0] - 1], (self.enfeites[(x, y)][1][0] - self.offset_x, self.enfeites[(x, y)][1][1] - self.offset_y))
    
    def render_trunk(self):
        for tree in Parede.paredes:
            tree.desenhar_tronco(self.offset_x, self.offset_y)
        
    def render_mage(self):
        self.mago.desenhar_mago(self.janela, self.offset_x, self.offset_y)

    def render_leaves(self):
        for tree in Parede.paredes:
            tree.desenhar_folhas(self.offset_x, self.offset_y)
      
    def render_hud(self):

        self.ratio_stamina = self.mago.stamina / 1000
        self.ratio_habilidade = self.mago.cooldown_habilidade / 270
        self.ratio_vida = self.mago.vida / 1000

        self.janela.blit(self.hud, (-200, self.camera_config["altura_camera"] - 60))
         #Fundo barra de stamina
        pg.draw.rect(
            self.janela, 
            self.color_config["CINZA"], 
            (
                self.x_barras, 
                self.y_barra_stamina, 
                self.hud_config["largura_barra"], 
                self.hud_config["altura_barra"] 
            ), 
            border_radius=self.hud_config["raio_borda"]
        )

        #Fundo barra de vida
        pg.draw.rect(
            self.janela, 
            self.color_config["CINZA"], 
            (   
                self.x_barras, 
                self.y_barra_vida, 
                self.hud_config["largura_barra"], 
                self.hud_config["altura_barra"]
            ), 
            border_radius=self.hud_config["raio_borda"]
        )

        # Barra de vida
        pg.draw.rect(
            self.janela, 
            self.color_config["VERDE"], 
            (
                self.x_barras, 
                self.y_barra_vida, 
                self.hud_config["largura_barra"] * self.ratio_vida, 
                self.hud_config["altura_barra"]
            ),  
            border_radius=self.hud_config["raio_borda"]
        )
        
        pg.draw.rect(
            self.janela, 
            self.color_config["BRANCO"], 
            (
                self.x_barras + 1, 
                self.y_barra_vida, 
                (self.hud_config["largura_barra"] - 2) * self.ratio_vida, 
                self.hud_config["altura_barra"] - 11
            ), 
            border_radius=self.hud_config["raio_borda"]
        )
        pg.draw.rect(
            janela, 
            self.color_config["MARROM_ESCURO"], 
            (
                self.x_barras, 
                self.y_barra_vida, 
                self.hud_config["largura_barra"], 
                self.hud_config["altura_barra"]
            ), self.hud_config["espessura"], 
            border_radius=self.hud_config["raio_borda"]
        )

        # Barra de stamina
        pg.draw.rect(
            self.janela, 
            self.color_config["AMARELO"], 
            (
                self.x_barras, 
                self.y_barra_stamina, 
                self.hud_config["largura_barra"] * self.ratio_stamina, 
                self.hud_config["altura_barra"]
            ), 
            border_radius=self.hud_config["raio_borda"]
        )
        pg.draw.rect(
            self.janela, 
            self.color_config["MARROM_ESCURO"], 
            (
                self.x_barras, 
                self.y_barra_stamina, 
                self.hud_config["largura_barra"], 
                self.hud_config["altura_barra"]
            ), 
            self.hud_config["espessura"], 
            border_radius=self.hud_config["raio_borda"]
        )

        #Visual do poder no hud
        poder_atual = self.fonte_tempo.render('Poder atual:', True, self.color_config["BRANCO"]) #texto, situação de aparecimento, cor
        janela.blit(poder_atual, (self.camera_config["largura_camera"] - poder_atual.get_width() - 900, self.camera_config["altura_camera"] - 45))
        
        if self.mago.poder:
            if len(self.cargas_hud) < 1:
                self.cargas_hud.append(Projectile_hud(self.mago.poder, self.poderes[self.mago.poder]))
            functions.draw_poder_hud(self.cargas_hud, self.janela)

            if self.tempo_poder == 0:
                barra_poder_largura = 100
            else:
                barra_poder_largura = self.tempo_poder

            pg.draw.rect(
                self.janela, 
                self.color_config["CINZA"], 
                (   
                    380, 
                    710, 
                    100, 
                    10
                ), 
                border_radius=self.hud_config["raio_borda"]
            )
            
            pg.draw.rect(
                self.janela, 
                self.color_config["AZUL"], 
                (
                    380, 
                    710, 
                    barra_poder_largura, 
                    10
                ), 
                border_radius=self.hud_config["raio_borda"]
            )

            pg.draw.rect(
                self.janela, 
                self.color_config["MARROM_ESCURO"], 
                (
                    380, 
                    710, 
                    100, 
                    10
                ), 
                self.hud_config["espessura"], 
                border_radius=self.hud_config["raio_borda"]
            )
            
        else:
            self.cargas_hud = []
        
        #Timer e contadores
        tempo_atual = time.time()
        tempo_passado = tempo_atual - self.comeco_timer
        self.tempo_restante = max(0, self.duracao_timer - tempo_passado) #evite com que o timer dê errado quando acabe
        minutos, segundos = divmod(int(self.tempo_restante), 60) #faz a divisão correta entre minutos e segundos
        texto_timer = self.fonte_tempo.render(f'Tempo: {minutos:02d}:{segundos:02d}', True, self.color_config["BRANCO"]) #texto, situação de aparecimento, cor
        janela.blit(texto_timer, (self.camera_config["largura_camera"] - texto_timer.get_width() - 15, self.camera_config["altura_camera"] - 45))
        x_inicial = self.camera_config["largura_camera"] - texto_timer.get_width() - 150
        
        #Blitando os sprites do animais no contador
        janela.blit(self.animal1_idle, (x_inicial - 200, self.camera_config["altura_camera"] - 48))
        janela.blit(self.animal2_idle, (x_inicial - 100, self.camera_config["altura_camera"] - 50))
        janela.blit(self.animal3_idle, (x_inicial, self.camera_config["altura_camera"] - 50))

        for animal in reversed(self.pontos_animais.keys()): #contador dos animais
            if self.pontos_animais[animal] < 10:
                contador = self.fonte_contador.render(f'x0{self.pontos_animais[animal]}', True, self.color_config["BRANCO"])
            else:
                contador = self.fonte_contador.render(f'x{self.pontos_animais[animal]}', True, self.color_config["BRANCO"]) 
            self.janela.blit(contador, (x_inicial + 32, altura_camera - 62))
            x_inicial -= 100

    def clear_game(self):
        Parede.paredes = []
        Animais.animais_vivos = []
        Animais.animais_mortos = []
        Coletaveis.coletaveis_ativos = []
        Dragao.dragoes_vivos = []
        self.cargas_dragao = []
        self.cargas = []
        Rio.rios = []
        self.tilemap = []
        self.mapa = {}
        self.desenho_enfeites = []
        self.enfeites = {}
        self.tempo_restante = 60
        self.duracao_timer = 60
        self.comeco_timer = time.time()
