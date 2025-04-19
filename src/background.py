from src.utils import create_sprite
from configs import *
from pygame import Vector2
from typing import List
import pygame.transform
import random
import os


class PipePair:
    def __init__(self, x):
        self._x = x
        self._gap = 150
        self._scored = False
        self._width = pygame.image.load(SPRITE_PATH + "pipe-green.png").get_width()
        self._height = pygame.image.load(SPRITE_PATH + "pipe-green.png").get_height()
        self._top_height = random.randint(50, SCREEN_HEIGHT - self._gap - 162) # avoid floor
        self._bottom_y = self._top_height + self._gap
        self._pipe_img = pygame.image.load(os.path.join(SPRITE_PATH, "pipe-green.png"))

    def move(self, speed) -> None:
        """
        Move the pipe to the left by a given speed.

        :param speed: The number of pixels to shift the pipe leftward.
        """
        self._x -= speed

    def draw(self, screen) -> None:
        """
        Draw the top and bottom pipes on the screen.

        :param screen: The surface where the pipes should be rendered.
        """
        # Top pipe
        top_pipe = pygame.transform.rotate(self._pipe_img, 180)
        screen.blit(top_pipe, (self._x, self._top_height - self._height))

        screen.blit(self._pipe_img, (self._x, self._bottom_y))

    @property
    def is_off_screen(self) -> bool:
        """
        Check whether the pipe has moved off the screen.

        :return: True if the pipe is completely off the left edge of the screen.
        """
        return self._x < -42

    @property
    def pos_x(self) -> int:
        return self._x

    @property
    def width(self) -> int:
        return self._width

    @property
    def bottom_y(self) -> int:
        return self._bottom_y

    @property
    def top_height(self) -> int:
        return self._top_height

    @property
    def scored(self) -> bool:
        return self._scored

    @scored.getter
    def scored(self) -> bool:
        return self._scored

    @scored.setter
    def scored(self, value: bool) -> None:
        self._scored = value



"""This Class represents all background of the game"""
class Background:
    # Constructor. Pass screen buffer;
    def __init__(self, screen):
        self._x = 0
        self._screen = screen

        # Sprites (background and floor)
        self.background = create_sprite(SPRITE_PATH, "background.png")
        self.floor = create_sprite(SPRITE_PATH, "floor.png")
        self.pipe_green = create_sprite(SPRITE_PATH, "pipe-green.png")

        self._pipe_timer = 0
        self._pipes = []
        self.pipe_speed = 2

    def draw(self, current_state: GameState) -> None:
        # Background
        self._screen.blit(self.background, (self._x, 0))
        self._screen.blit(self.background, (self._x + SCREEN_WIDTH, 0))

        if current_state == GameState.PLAYING or current_state == GameState.GAME_OVER:
            self.draw_pipes(current_state)

        # Floor
        self._screen.blit(self.floor, (self._x, (SCREEN_HEIGHT - 112)))
        self._screen.blit(self.floor, (self._x + SCREEN_WIDTH, (SCREEN_HEIGHT - 112)))

        if not current_state == GameState.GAME_OVER:
            self._x -= 1
            if self._x <= -self.background.get_width():
                self._x = 0


    def draw_pipes(self, current_state: GameState):
        self._pipe_timer += 1
        if self._pipe_timer % 90 == 0 and not current_state == GameState.GAME_OVER:
            self._pipes.append(PipePair(SCREEN_WIDTH))

        for pipe in self._pipes:
            if not current_state == GameState.GAME_OVER:
                pipe.move(self.pipe_speed)
            pipe.draw(self._screen)

        if not current_state == GameState.GAME_OVER:
            new_pipes = []
            for pipe in self._pipes:
                if not pipe.is_off_screen:
                    new_pipes.append(pipe)

            self._pipes = new_pipes

    def reset(self):
        self._pipes = []
        self._pipe_timer = 0

    @property
    def get_pipes(self) -> List[PipePair]:
        return self._pipes
