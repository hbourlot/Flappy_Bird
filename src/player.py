from pygame import Vector2
from typing import List
from configs import *
from pygame import Surface
from pygame import mixer
from src.background import PipePair
from src.utils import create_sprite
import os.path
import pygame

class Player:
    # Constructor. Pass the screen buffer
    def __init__(self, screen):
        self._player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        self._original_pos = self._player_pos.copy()
        self._screen = screen # Screen buffer

        self._angle = 0
        self._rotation_speed = 2
        self._max_rotation = 30
        self._fall_rotation_speed = 1
        self.velocity = pygame.Vector2(0, 0)

        # Load original sprites
        self.original_b1 = create_sprite(SPRITE_PATH, "redbird-downflap.png")
        self.original_b2 = create_sprite(SPRITE_PATH, "redbird-midflap.png")
        self.original_b3 = create_sprite(SPRITE_PATH, "redbird-upflap.png")

        #Current sprite (rotated version)
        self.b1 = self.original_b1 # Rotated sprite
        self.b2 = self.original_b2 # Rotated sprite
        self.b3 = self.original_b3 # Rotated sprite
        self.current_sprite = self.original_b1

        # Player frame
        self._timer = 0
        self._animation_speed = 0.09 # seconds per frame
        self._sprite_idx = 0
        self._last_time = pygame.time.get_ticks() / 1000.0
        self._sprites = [self.b1, self.b2, self.b3]




    @staticmethod
    def rotate_sprite(sprite, angle) -> Surface:
        """
        Rotates the given sprite image by a specific angle using smooth scaling.

        :param sprite: The surface (image) to rotate.
        :param angle: The rotation angle in degrees. Positive is counter-clockwise.
        :return: A new, rotated surface.
        """
        rotate = pygame.transform.rotozoom(sprite, angle, 1)
        return rotate

    def update_rotation(self, is_flapping=False):
        """
        Updates the rotation angle and rotated sprites based on the player movement.

        :param is_flapping: True if the bird is flapping, False if it's falling.
        """
        if is_flapping:
            # Rotate upward (negative angle) when flapping
            self._angle = max(self._angle - self._rotation_speed, self._max_rotation)
        else:
            # Rotate downward (positive angle) when falling
            self._angle = min(self._angle - self._rotation_speed, self._max_rotation)

        self.b1 = self.rotate_sprite(self.original_b1, self._angle)
        self.b2 = self.rotate_sprite(self.original_b2, self._angle)
        self.b3 = self.rotate_sprite(self.original_b3, self._angle)
        self._sprites = [self.b1, self.b2, self.b3]

    def draw(self, current_state: GameState) -> None:
        """
        Draws the player sprite depending on the game state.

        :param current_state: Current state of the game (MENU, PLAYING, etc.)
        """
        if current_state == GameState.MENU:
            return
        # Get rect with center position
        sprite_rect = self.current_sprite.get_rect(center=self._player_pos)
        if current_state == GameState.PLAYING:
            self.update(current_state)
        self._screen.blit(self.current_sprite, sprite_rect.topleft)
        if current_state != GameState.PLAYING and pygame.key.get_pressed()[pygame.K_SPACE]:
            # Draw the rotated sprite
            self._screen.blit(self.current_sprite, sprite_rect.topleft)
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.reset()

    def flap(self) -> None:
        """
        Makes the player 'flap' (jump). Called when the player presses the flap key.
        """
        self.audio_score()
        self.velocity.y = -5
        self.update_rotation(is_flapping=True)


    def update(self, current_state: GameState) -> None:
        """
        Updates player position, velocity, rotation, and sprite animation.

        :param current_state: Should be PLAYING when updating.
        """
        if current_state == GameState.PLAYING:
            # Apply Gravity
            self.velocity.y += 0.2
            self._player_pos += self.velocity

            now = pygame.time.get_ticks() / 1000
            delta = now - self._last_time

            if delta >= self._animation_speed:
                self._sprite_idx = (self._sprite_idx + 1) % len(self._sprites)
                self.current_sprite = self._sprites[self._sprite_idx]
                self._last_time = now

            # Update rotation based on vertical velocity
            if self.velocity.y > 0: # Falling
                self.update_rotation(is_flapping=False)
            elif self.velocity.y < 0: # Rising
                self.update_rotation(is_flapping=True)

    def has_died(self, floor_gap: int, pipes: List[PipePair]) -> bool:
        """
        Checks if the player has collided with the ground, ceiling, or a pipe.

        :param floor_gap: Height from bottom where ground is considered.
        :param pipes: List of pipe obstacles to check for collision.
        :return: True if the player has died.
        """
        if self._player_pos.y >= (SCREEN_HEIGHT - floor_gap) or self._player_pos.y <= 0:
            self.audio_hit()
            return True

        player_rect = self.current_sprite.get_rect(center=self._player_pos)
        for pipe in pipes:
            # Top pipe rect (flipped)
            top_rect = pygame.Rect(pipe.pos_x, 0, pipe.width, pipe.top_height)
            # Bottom pipe rect
            bottom_rect = pygame.Rect(pipe.pos_x, pipe.bottom_y, pipe.width, SCREEN_HEIGHT - pipe.bottom_y)

            if player_rect.colliderect(top_rect) or player_rect.colliderect(bottom_rect):
                    self.audio_hit()
                    return True
        return False

    def reset(self) -> None:
        """
        Resets the player state (position, velocity, and rotation).
        Called after death or when restarting.
        """
        self._player_pos = self._original_pos.copy()
        self.velocity = pygame.Vector2(0, 0)
        self._angle = 0
        self.current_sprite = self.original_b1

    @staticmethod
    def audio_score() -> None:
        mixer.music.load(os.path.join(AUDIO_PATH, "wing.wav"))
        mixer.music.play()

    @staticmethod
    def audio_hit() -> None:
        mixer.music.load(os.path.join(AUDIO_PATH, "hit.wav"))
        mixer.music.play()

    @property
    def player_pos(self) -> Vector2:
        return self._player_pos

    @player_pos.getter
    def player_pos(self) -> Vector2:
        return self._player_pos

    @player_pos.setter
    def player_pos(self, value: Vector2) -> None:
        self._player_pos = value

