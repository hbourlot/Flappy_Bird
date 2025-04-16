import os
import pygame

def create_sprite(path, sprite_name):
    return pygame.image.load(os.path.join(path, sprite_name))


