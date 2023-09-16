from objects import Vector2d

global_config = {
    "screen_config": {
        "screen_width": 1200,
        "screen_height": 650,
        "tps": 60, # ticks por segundo
    },
   "player_config": {
        "position": Vector2d(200, 200),
        "initial_direction": Vector2d(0, 0),
        "dimension": Vector2d(75, 75),
        "speed": 2,
        "stamina": 1000,
   },
   "animal_config": {
        "spawn_rate": 5,
        "speed": 1,
   },
   "colors_config": {
        "WHITE": (255, 255, 255),
        "GREEN": (0, 230, 0),
        "BLACK": (0, 0, 0),
        "YELLOW": (255, 255, 0),
        "RED": (255, 0, 0),
        "BLUE": (95,159,159),
        "LIGHT_BLUE": (173,216,230),
        "BROWN": (210, 180, 140),
        "DARK_BROWN": (123, 66, 48),
        "GRAY": (211,211,211),
   }
}