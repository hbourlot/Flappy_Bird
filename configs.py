from enum import auto, Enum

SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
FPS = 60
SPRITE_PATH = "./assets/sprites/"
AUDIO_PATH = "./assets/audios/"


class GameState(Enum):
    MENU = auto() # 1
    PLAYING = auto() # 2
    GAME_OVER = auto() # 3
    PAUSE = auto() # 4
