from configs import *
from src.utils import create_sprite
import pygame

class Player:
    # Constructor. Pass the screen buffer
    def __init__(self, screen):
        self.alive = True # State of player
        self.player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        self.original_pos = self.player_pos.copy()
        self.screen = screen # Screen buffer

        self.angle = 0
        self.rotation_speed = 2
        self.max_rotation = 30
        self.fall_rotation_speed = 1

        # Load original sprites
        self.original_b1 = create_sprite(SPRITE_PATH, "redbird-downflap.png")
        self.original_b2 = create_sprite(SPRITE_PATH, "redbird-midflap.png")
        self.original_b3 = create_sprite(SPRITE_PATH, "redbird-upflap.png")
        self.game_over = create_sprite(SPRITE_PATH, "gameover.png")

        #Current sprite (rotated version)
        self.b1 = None # Rotated sprite
        self.b2 = None # Rotated sprite
        self.b3 = None # Rotated sprite
        self.current_sprite = self.original_b1
        self.velocity = pygame.Vector2(0, 0)


    @staticmethod
    def rotate_sprite(sprite, angle):
        """Rotate a sprite while maintaining its center position"""
        rotate_sprite = pygame.transform.rotozoom(sprite, angle, 1)
        return rotate_sprite

    def update_rotation(self, is_flapping=False):
        """Update the player's rotation based on movement"""
        if is_flapping:
            # Rotate upward (negative angle) when flapping
            self.angle = max(self.angle - self.rotation_speed, self.max_rotation)
        else:
            # Rotate downward (positive angle) when falling
            self.angle = min(self.angle - self.rotation_speed, self.max_rotation)

        self.b1 = self.rotate_sprite(self.original_b1, self.angle)
        self.b2 = self.rotate_sprite(self.original_b2, self.angle)
        self.b3 = self.rotate_sprite(self.original_b3, self.angle)

    def draw(self):

        self.dead_state()
        if self.alive:
            # Get the current sprite
            current_sprite = self.b1

            # Get rect with center position
            sprite_rect = current_sprite.get_rect(center=self.player_pos)

            # Draw the rotated sprite
            self.screen.blit(current_sprite, sprite_rect.topleft)
        else:
            # Getting middle rect position
            sprite_rect = self.game_over.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            self.screen.blit(self.game_over, sprite_rect)
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.alive = True
                self.player_pos = self.original_pos.copy()


    def flap(self):
        """Called when player flaps/jumps"""
        self.velocity.y = -5
        self.update_rotation(is_flapping=True)

    def update(self):
        """Update player position and rotation"""
        # Apply Gravity
        self.velocity.y += 0.2
        self.player_pos += self.velocity

        # Update rotation based on vertical velocity
        if self.velocity.y > 0: # Falling
            self.update_rotation(is_flapping=False)
        elif self.velocity.y < 0: # Rising
            self.update_rotation(is_flapping=True)

    def dead_state(self):

        if self.player_pos.y >= SCREEN_HEIGHT:
            self.alive = False
        else:
            self.alive = True

    # def timing_dead(self):




