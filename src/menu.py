from configs import *
from src.utils import create_sprite
import pygame


class Menu:
    def __init__(self):
        self.running = True
        self.y = SCREEN_HEIGHT / 2
        self.x = SCREEN_WIDTH / 2
        self.img = create_sprite(SPRITE_PATH, "message.png")
        self.state = True

    def draw(self, screen):
        self.start_menu(screen)

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

    def start_menu(self, screen):
        if self.running:
            screen.blit(self.img, (self.x / 2.5, self.y / 2))
            pygame.time.Clock().tick(FPS) / 2000
            self.running = self.space_signal()
            return self.esq_signal()