import pygame as pg
info = pg.display.Info()

# Retrieve the screen width and height
screen_width = info.current_w
screen_height = info.current_h

global_config = {
    "color_config": {
        "BRANCO": (255, 255, 255),
        "VERDE": (0, 230, 0),
        "PRETO": (0, 0, 0),
        "AMARELO": (255, 255, 0),
        "VERMELHO": (255, 0, 0),
        "AZUL": (95,159,159),
        "AZUL_CLARO": (173,216,230),
        "MARROM": (210, 180, 140),
        "MARROM_ESCURO": (123, 66, 48),
        "CINZA": (211,211,211),
    },
    "screen_config": {
        "LARGURA_MAPA": 1280 * 2,
        "ALTURA_MAPA": 720 * 2,
        "tela_cheia": False,
    },
    "camera_config": {
        "largura_camera": screen_width,
        "altura_camera": screen_height,
    },
    "animal_config": {
        "num_animais": 3,
        "num_frames": 3,
    },
    "speed_config": {
        "velocidade_devagar": 0.05,
        "velocidade_padrao": 0.0575,
        "velocidade_rapida": 0.065,
    },
    "player_config": {
        "stamina_padrao": 1000,
        "cooldown_habilidade_padrao": 270,
        "vida_padrao": 1000,
        "ponto_inicial": (100, 100),
    },
    "map_config": {
        "num_tiles": 35,
        "num_enfeites": 11,
    },
    "hud_config": {
        "largura_barra": 200,
        "largura_barra_skill": 64,
        "altura_barra": 15,
        "altura_barra_habilidade": 48,
        "raio_borda": 4,
        "espessura": 2,
    }
}


"""
 ratio_stamina = mago.stamina / 1000
    ratio_habilidade = mago.cooldown_habilidade / 270
    ratio_vida = mago.vida / 1000

    "hud_config": {  
        largura_barra = 200
        largura_barra_skill = 64
        altura_barra = 15
        altura_barra_habilidade = 48
        raio_borda = 4
        espessura = 2
        x_barras = largura_camera / (largura_camera/10)
        y_barra_stamina = altura_camera / (altura_camera/(altura_camera - 28))
        y_barra_vida = altura_camera / (altura_camera/(altura_camera - 44))
        x_barra_habilidade = largura_camera / (largura_camera / 270)
        y_barra_habilidade = y_barra_vida - 9}
    


   
    duracao_timer = 60 #em segundos
"""