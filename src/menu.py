from configs import *
from src.utils import create_sprite
import pygame


class Menu:
    def __init__(self, screen):
        self.running = True
        self.y = SCREEN_HEIGHT / 2
        self.x = SCREEN_WIDTH / 2
        self.img = create_sprite(SPRITE_PATH, "message.png")
        self.game_over_sprite = create_sprite(SPRITE_PATH, "gameover.png")
        self.state = True
        self.screen = screen

    # def draw(self):
    #     self.start()
    #     # return self

    @staticmethod
    def space_signal():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return False
        return True

    @staticmethod
    def esq_signal():
        """Handling ESQ key to close the game"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return False
        return True

    def start(self):
        if self.running:
            self.screen.blit(self.img, (self.x / 2.5, self.y / 2))
            pygame.time.Clock().tick(FPS) / 2000

    def game_over(self):
        if self.running:
            sprite_rect = self.game_over_sprite.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            self.screen.blit(self.game_over_sprite, sprite_rect)

