from configs import *
from src.utils import create_sprite

"""This Class represents all background of the game"""
class Background:
    # Constructor. Pass screen buffer;
    def __init__(self, screen):
        self.x = 0
        self.screen = screen

        # Sprites (background and floor)
        self.background = create_sprite(SPRITE_PATH, "background.png")
        self.floor = create_sprite(SPRITE_PATH, "floor.png")

    def draw(self):
        # Background
        self.screen.blit(self.background, (self.x, 0))
        self.screen.blit(self.background, (self.x + SCREEN_WIDTH, 0))

        # Floor
        self.screen.blit(self.floor, (self.x, (SCREEN_HEIGHT - 112)))
        self.screen.blit(self.floor, (self.x + SCREEN_WIDTH, (SCREEN_HEIGHT - 112)))
        self.x -= 1
        if self.x <= -self.background.get_width():
            self.x = 0




